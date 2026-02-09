import os
import json
from flask import Flask, request, jsonify, render_template_string, session
from google import genai
from google.genai import types

app = Flask(__name__)
app.secret_key = "smile_ai_ultra_premium_fix"

# --- GOOGLE AUTH SETUP ---
#
json_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if json_creds:
    with open("google_key.json", "w") as f:
        f.write(json_creds)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("google_key.json")

PROJECT_ID = "smile-ai-486910" 

@app.route('/login-sync', methods=['POST'])
def login_sync():
    session['logged_in'] = True
    return jsonify({"status": "success"})

@app.route('/ask-ai', methods=['POST'])
def ask_ai():
    user_query = request.json.get('query', "")
    try:
        # Vertex AI Client
        client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_query,
            config=types.GenerateContentConfig(
                system_instruction="You are Smile Financial Solution AI, built by Smile Financial Solution Company. You are an expert in Finance and Business. Always be professional. Never mention Google or Gemini."
            )
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "System busy. Please try again later."})

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Smile AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://accounts.google.com/gsi/client" async defer></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&display=swap');
        body { background: #ffffff; font-family: 'Google Sans', sans-serif; height: 100vh; display: flex; flex-direction: column; margin: 0; }
        .header { padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f1f1; background: #fff; }
        .visit-site { color: #1a73e8; border: 1px solid #1a73e8; padding: 6px 16px; border-radius: 20px; font-size: 14px; font-weight: 500; text-decoration: none; }
        
        #chat-area { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 24px; }
        .welcome-text { font-size: 32px; color: #1f1f1f; font-weight: 400; margin-top: 40px; }
        .sub-text { color: #70757a; font-size: 18px; margin-top: 8px; }
        
        .input-container { padding: 16px; background: #fff; }
        .input-box { background: #f0f4f9; border-radius: 32px; padding: 12px 20px; display: flex; align-items: center; gap: 15px; max-width: 800px; margin: 0 auto; }
        .input-box input { flex: 1; background: transparent; border: none; outline: none; font-size: 16px; color: #1f1f1f; }
        
        .user-bubble { background: #e9eef6; padding: 12px 20px; border-radius: 22px; align-self: flex-end; max-width: 85%; color: #1f1f1f; font-size: 16px; }
        .ai-response { display: flex; gap: 15px; align-items: flex-start; }
        .ai-icon { width: 30px; height: 30px; background: #1a73e8; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: bold; flex-shrink: 0; }
        
        .pill { border: 1px solid #dadce0; padding: 10px 20px; border-radius: 25px; background: #fff; font-size: 14px; color: #3c4043; cursor: pointer; transition: 0.2s; white-space: nowrap; }
        .pill:hover { background: #f8f9fa; }
    </style>
</head>
<body>
    {% if not logged_in %}
    <div class="flex-1 flex flex-col justify-center items-center p-8 text-center">
        <div class="w-20 h-20 bg-blue-600 rounded-3xl flex items-center justify-center text-white text-4xl font-bold mb-6">S</div>
        <h1 class="text-3xl font-bold">Smile Financial <span class="text-blue-600">AI</span></h1>
        <p class="text-gray-500 mt-4 mb-10">नमस्ते! अपनी कंपनी के AI में लॉगिन करें।</p>
        <div id="g_id_onload" data-client_id="434178553524-ebqcdglqghl6op8jj92i0vtqgpnj7uku.apps.googleusercontent.com" data-callback="onSignIn"></div>
        <div class="g_id_signin" data-type="standard" data-shape="pill"></div>
    </div>
    {% else %}
    <div class="header">
        <div class="flex items-center gap-4">
            <i class="fa-solid fa-bars text-gray-500 text-xl"></i>
            <span class="text-xl font-medium">Smile AI</span>
        </div>
        <div class="flex items-center gap-4">
            <a href="https://smilefinancial.in" target="_blank" class="visit-site">Visit Site</a>
            <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">M</div>
        </div>
    </div>

    <main id="chat-area">
        <div id="welcome-screen">
            <div class="welcome-text">नमस्ते Mohmmad</div>
            <div class="sub-text">मैं Smile Financial Solution AI हूँ, आज आपकी क्या सहायता करूँ?</div>
            <div class="flex gap-2 mt-10 overflow-x-auto pb-4 no-scrollbar">
                <button onclick="quick('Business Plan')" class="pill">📊 Business Plan</button>
                <button onclick="quick('Financial Support')" class="pill">💰 Financial Support</button>
            </div>
        </div>
        <div id="msg-list" class="flex flex-col gap-6"></div>
    </main>

    <div class="input-container">
        <div class="input-box">
            <i class="fa-solid fa-plus text-gray-400 text-xl cursor-pointer"></i>
            <input type="text" id="userInput" placeholder="Smile AI से पूछें..." autocomplete="off">
            <i class="fa-solid fa-microphone text-gray-400 text-xl cursor-pointer" id="mic-icon"></i>
            <button id="sendBtn" class="hidden text-blue-600" onclick="sendMsg()"><i class="fa-solid fa-paper-plane text-xl"></i></button>
        </div>
        <div class="text-[10px] text-center text-gray-400 mt-2">Developed by Smile Financial Solution Company</div>
    </div>
    {% endif %}

    <script>
        function onSignIn(r) {
            fetch('/login-sync', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({token:r.credential})})
            .then(() => window.location.reload());
        }

        const input = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');
        const micIcon = document.getElementById('mic-icon');

        input?.addEventListener('input', () => {
            const hasVal = input.value.trim() !== "";
            sendBtn.classList.toggle('hidden', !hasVal);
            micIcon.classList.toggle('hidden', hasVal);
        });

        async function sendMsg() {
            const val = input.value.trim();
            if(!val) return;
            
            document.getElementById('welcome-screen').style.display = 'none';
            const list = document.getElementById('msg-list');
            list.innerHTML += `<div class="user-bubble">${val}</div>`;
            input.value = "";
            sendBtn.classList.add('hidden');
            micIcon.classList.remove('hidden');

            const aiId = "ai-" + Date.now();
            list.innerHTML += `<div class="ai-response" id="${aiId}"><div class="ai-icon">S</div><div class="text-gray-400 animate-pulse">Smile AI is thinking...</div></div>`;
            
            const area = document.getElementById('chat-area');
            area.scrollTop = area.scrollHeight;

            const res = await fetch('/ask-ai', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({query:val})});
            const data = await res.json();
            document.getElementById(aiId).innerHTML = `<div class="ai-icon">S</div><div class="text-gray-800 leading-relaxed">${data.reply}</div>`;
            area.scrollTop = area.scrollHeight;
        }
        function quick(t) { input.value = t; sendMsg(); }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
