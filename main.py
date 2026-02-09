import os
import json
import requests
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
from google import genai
from google.genai import types

app = Flask(__name__)
app.secret_key = "smile_financial_ai_exclusive"

# --- JSON KEY SETUP FOR RENDER ---
json_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if json_creds:
    with open("google_key.json", "w") as f:
        f.write(json_creds)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("google_key.json")

PROJECT_ID = "smile-ai-486910"

# --- SYSTEM PROMPT (Identity Fixing) ---
# Yahan AI ko uski pehchan sikhayi ja rahi hai
SYSTEM_INSTRUCTION = """
You are 'Smile Financial Solution AI', developed by 'Smile Financial Solution Company'. 
Never mention Google or Gemini. Your purpose is to provide Financial Support, Business Planning, 
and general assistance. You know everything about Smile Financial Solution's services 
(Loans, Insurance, Investment planning, Business Growth). Always greet users politely 
as a representative of Smile Financial Solution.
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Smile Financial Solution AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&display=swap');
        
        :root { --primary-blue: #1a73e8; --bg-gray: #f8fafd; }
        
        body { 
            background: var(--bg-gray); 
            font-family: 'Google Sans', sans-serif; 
            height: 100vh; 
            margin: 0;
            display: flex; 
            flex-direction: column;
            -webkit-tap-highlight-color: transparent;
        }

        /* Responsive Header */
        header { 
            background: white; 
            padding: 12px 16px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            border-bottom: 1px solid #eee;
            position: sticky; top: 0; z-index: 50;
        }

        .visit-site-btn {
            font-size: 12px;
            color: var(--primary-blue);
            border: 1px solid var(--primary-blue);
            padding: 4px 12px;
            border-radius: 16px;
            font-weight: 500;
        }

        /* Chat Layout */
        main { flex: 1; overflow-y: auto; padding: 16px; scroll-behavior: smooth; }
        .welcome-text { font-size: 28px; line-height: 1.2; color: #1f1f1f; margin-top: 20px; }
        .sub-text { color: #70757a; font-size: 16px; margin-top: 8px; }

        /* Gemini-style Pills */
        .pill-container { display: flex; gap: 8px; overflow-x: auto; padding: 16px 0; scrollbar-width: none; }
        .pill { 
            background: white; border: 1px solid #dadce0; 
            padding: 10px 18px; border-radius: 24px; 
            white-space: nowrap; font-size: 14px; cursor: pointer;
        }

        /* Gemini-style Keyboard Area */
        .bottom-nav { 
            background: white; 
            padding: 12px 16px env(safe-area-inset-bottom); 
            border-top: 1px solid #f1f1f1;
        }
        
        .input-box {
            background: #f0f4f9;
            border-radius: 28px;
            padding: 8px 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .input-box input {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            font-size: 16px;
            padding: 8px 0;
            color: #1f1f1f;
        }

        .icon-btn { color: #5f6368; font-size: 20px; cursor: pointer; transition: 0.2s; }
        .icon-btn:hover { color: var(--primary-blue); }
        
        #send-btn { color: var(--primary-blue); display: none; }

        .ai-response { display: flex; gap: 12px; margin-top: 24px; }
        .ai-icon { width: 30px; height: 30px; filter: hue-rotate(200deg); }
        .user-msg { background: #e9eef6; padding: 12px 18px; border-radius: 20px; align-self: flex-end; max-width: 85%; }
        
        .thinking { font-size: 12px; color: var(--primary-blue); margin-bottom: 4px; display: none; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="flex-1 flex flex-col justify-center items-center bg-white p-8">
        <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d473530c2731a4cd0247d.svg" class="w-20 mb-6 ai-icon">
        <h1 class="text-3xl font-bold text-gray-800">Smile Financial <span class="text-blue-600">AI</span></h1>
        <p class="text-gray-500 mt-4 mb-10">Namaste! Login to access your financial assistant.</p>
        <div id="g_id_onload" data-client_id="434178553524-ebqcdglqghl6op8jj92i0vtqgpnj7uku.apps.googleusercontent.com" data-callback="handleCredentialResponse"></div>
        <div class="g_id_signin" data-type="standard"></div>
    </div>
    {% else %}

    <header>
        <div class="flex items-center gap-3">
            <i class="fa-solid fa-bars text-gray-500"></i>
            <span class="font-medium text-lg">Smile AI</span>
        </div>
        <a href="https://yourcompany.com" target="_blank" class="visit-site-btn">Visit Site</a>
    </header>

    <main id="chat-container">
        <div id="welcome-ui">
            <div class="welcome-text">नमस्ते Mohmmad</div>
            <div class="sub-text">मैं Smile Financial Solution AI हूँ, आज मैं आपकी क्या सहायता कर सकता हूँ?</div>
            
            <div class="pill-container">
                <div class="pill" onclick="sendQuick('Business Planning help')">📊 Business Planning</div>
                <div class="pill" onclick="sendQuick('Financial support options')">💰 Financial Support</div>
                <div class="pill" onclick="sendQuick('Create a professional image')">🖼️ Create Image</div>
            </div>
        </div>
        <div id="chat-messages" class="flex flex-col gap-4"></div>
    </main>

    <div class="bottom-nav">
        <div class="input-box">
            <label for="file-up" class="icon-btn"><i class="fa-solid fa-plus"></i></label>
            <input type="file" id="file-up" class="hidden">
            
            <input type="text" id="user-input" placeholder="Smile AI से पूछें..." autocomplete="off">
            
            <i class="fa-solid fa-microphone icon-btn" id="mic-btn"></i>
            <button id="send-btn" onclick="handleSend()"><i class="fa-solid fa-paper-plane"></i></button>
        </div>
        <div class="text-[10px] text-center text-gray-400 mt-2">Developed by Smile Financial Solution Company</div>
    </div>

    {% endif %}

    <script>
        const input = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');
        const micBtn = document.getElementById('mic-btn');

        input?.addEventListener('input', () => {
            const hasVal = input.value.trim() !== "";
            sendBtn.style.display = hasVal ? 'block' : 'none';
            micBtn.style.display = hasVal ? 'none' : 'block';
        });

        async function handleSend() {
            const text = input.value.trim();
            if(!text) return;
            
            document.getElementById('welcome-ui').style.display = 'none';
            addMessage(text, 'user');
            input.value = "";
            sendBtn.style.display = 'none';
            micBtn.style.display = 'block';

            const loadingId = addMessage("Smile AI is thinking...", 'ai', true);

            try {
                const res = await fetch('/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: text})
                });
                const data = await res.json();
                updateAI(loadingId, data.reply);
            } catch (e) {
                updateAI(loadingId, "Maaf kijiye, connection mein dikkat hai.");
            }
        }

        function addMessage(text, sender, isLoading = false) {
            const container = document.getElementById('chat-messages');
            const id = "msg-" + Date.now();
            if(sender === 'user') {
                container.innerHTML += `<div class="user-msg">${text}</div>`;
            } else {
                container.innerHTML += `
                    <div class="ai-response" id="${id}">
                        <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d473530c2731a4cd0247d.svg" class="ai-icon">
                        <div>
                            <div class="thinking" style="${isLoading ? 'display:block' : ''}">Thinking...</div>
                            <div class="ai-txt">${isLoading ? '...' : text}</div>
                        </div>
                    </div>`;
            }
            document.getElementById('chat-container').scrollTop = document.getElementById('chat-container').scrollHeight;
            return id;
        }

        function updateAI(id, text) {
            const el = document.getElementById(id);
            if(el) {
                el.querySelector('.thinking').style.display = 'none';
                el.querySelector('.ai-txt').innerText = text;
            }
        }

        function sendQuick(t) { input.value = t; handleSend(); }

        function handleCredentialResponse(response) {
            fetch('/google-login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({token: response.credential})
            }).then(() => window.location.reload());
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, logged_in=session.get('logged_in'))

@app.route('/google-login', methods=['POST'])
def google_login():
    session['logged_in'] = True
    return jsonify({"status": "success"})

@app.route('/ask', methods=['POST'])
def ask():
    q = request.json.get('query', "")
    try:
        client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
        # System Instruction se AI ki identity lock kar di gayi hai
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=q,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)
        )
        reply = response.text
    except:
        reply = "Smile Financial Solution AI is currently busy. Please try again."
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
