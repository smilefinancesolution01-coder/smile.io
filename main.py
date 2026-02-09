import os
import json
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
from google import genai
from google.genai import types

app = Flask(__name__)
app.secret_key = "smile_seamless_login_2026"

# --- JSON KEY SETUP ---
json_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if json_creds:
    with open("google_key.json", "w") as f:
        f.write(json_creds)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("google_key.json")

PROJECT_ID = "smile-ai-486910" #

# --- SYSTEM INSTRUCTION (Identity) ---
SYSTEM_INSTRUCTION = "You are Smile Financial Solution AI, created by Smile Financial Solution Company. Provide expert financial and business advice. Never mention Google or Gemini. Your interface and speed match the world's best AI."

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Smile Financial AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://accounts.google.com/gsi/client" async defer></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&display=swap');
        body { background: #f8fafd; font-family: 'Google Sans', sans-serif; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
        .input-area { background: #f0f4f9; border-radius: 32px; padding: 12px 20px; display: flex; align-items: center; gap: 15px; }
        .input-area input { flex: 1; background: transparent; border: none; outline: none; font-size: 16px; }
        .gemini-pill { border: 1px solid #dadce0; padding: 8px 16px; border-radius: 20px; background: white; font-size: 14px; white-space: nowrap; }
        #chat-scroller::-webkit-scrollbar { width: 0px; }
        .ai-icon { width: 32px; height: 32px; background: #1a73e8; color: white; border-radius: 50%; display: flex; items: center; justify-content: center; font-weight: bold; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="flex-1 flex flex-col justify-center items-center bg-white p-6">
        <div class="w-20 h-20 bg-blue-600 rounded-3xl flex items-center justify-center text-white text-4xl font-bold mb-6">S</div>
        <h1 class="text-3xl font-bold text-gray-800">Smile Financial <span class="text-blue-600">AI</span></h1>
        <p class="text-gray-500 mt-2 mb-10 text-center">Namaste! Click below to start instantly.</p>
        
        <div id="g_id_onload"
             data-client_id="434178553524-ebqcdglqghl6op8jj92i0vtqgpnj7uku.apps.googleusercontent.com"
             data-context="signin"
             data-ux_mode="popup"
             data-callback="onSignIn"
             data-auto_prompt="true">
        </div>
        <div class="g_id_signin" data-type="standard" data-shape="pill" data-theme="outline" data-text="signin_with" data-size="large"></div>
    </div>

    {% else %}
    <header class="p-4 flex justify-between items-center bg-white border-b border-gray-100">
        <div class="flex items-center gap-4">
            <i class="fa-solid fa-bars text-gray-500"></i>
            <span class="text-xl font-medium">Smile AI</span>
        </div>
        <div class="flex items-center gap-3">
            <a href="https://smilefinancial.in" target="_blank" class="text-blue-600 text-sm font-medium border border-blue-600 px-3 py-1 rounded-full">Visit Site</a>
            <div class="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center">M</div>
        </div>
    </header>

    <main id="chat-scroller" class="flex-1 overflow-y-auto p-6">
        <div id="home-view">
            <h1 class="text-4xl font-normal text-gray-800 leading-tight">नमस्ते Mohmmad<br><span class="text-gray-400">मैं Smile Financial AI हूँ, कैसे मदद करूँ?</span></h1>
            <div class="flex gap-2 mt-10 overflow-x-auto no-scrollbar">
                <button onclick="autoAsk('Business Plan')" class="gemini-pill">📊 Business Plan</button>
                <button onclick="autoAsk('Financial Help')" class="gemini-pill">💰 Financial Support</button>
            </div>
        </div>
        <div id="chat-box" class="space-y-8"></div>
    </main>

    <div class="p-4 bg-white">
        <div class="input-area max-w-3xl mx-auto">
            <label for="file-in" class="cursor-pointer text-gray-500 text-xl"><i class="fa-solid fa-plus"></i></label>
            <input type="file" id="file-in" class="hidden">
            <input type="text" id="user-input" placeholder="Smile AI से पूछें..." autocomplete="off">
            <i class="fa-solid fa-microphone text-gray-500 text-xl" id="mic-btn"></i>
            <button id="send-btn" onclick="send()" class="hidden text-blue-600 text-xl"><i class="fa-solid fa-paper-plane"></i></button>
        </div>
        <p class="text-[10px] text-center text-gray-400 mt-3">Smile Financial Solution Company © 2026</p>
    </div>
    {% endif %}

    <script>
        function onSignIn(response) {
            fetch('/login-api', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({token: response.credential})
            }).then(() => window.location.reload());
        }

        const input = document.getElementById('user-input');
        input?.addEventListener('input', () => {
            const hasText = input.value.trim() !== "";
            document.getElementById('send-btn').classList.toggle('hidden', !hasText);
            document.getElementById('mic-btn').classList.toggle('hidden', hasText);
        });

        async function send() {
            const text = input.value.trim();
            if(!text) return;
            document.getElementById('home-view').style.display = 'none';
            const box = document.getElementById('chat-box');
            box.innerHTML += `<div class="flex justify-end"><div class="bg-[#e9eef6] px-5 py-3 rounded-2xl max-w-[85%]">${text}</div></div>`;
            input.value = "";
            
            const aiId = "ai-" + Date.now();
            box.innerHTML += `<div class="flex gap-4" id="${aiId}"><div class="ai-icon">S</div><div class="text-gray-400 animate-pulse">Thinking...</div></div>`;
            
            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: text})
            });
            const data = await res.json();
            document.getElementById(aiId).innerHTML = `<div class="ai-icon">S</div><div class="leading-relaxed text-gray-800">${data.reply}</div>`;
        }
        function autoAsk(t) { input.value = t; send(); }
    </script>
</body>
</html>
"""

@app.route('/login-api', methods=['POST'])
def login_api():
    session['logged_in'] = True
    return jsonify({"status": "ok"})

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, logged_in=session.get('logged_in'))

@app.route('/ask', methods=['POST'])
def ask():
    q = request.json.get('query', "")
    try:
        client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=q,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)
        )
        reply = response.text
    except:
        reply = "Kshama karein, main abhi busy hoon. Kripya thodi der baad koshish karein."
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
