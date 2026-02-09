import os
import json
from flask import Flask, request, jsonify, render_template_string, session
from google import genai
from google.genai import types

app = Flask(__name__)
app.secret_key = "smile_financial_premium_2026"

# --- JSON KEY SETUP ---
json_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if json_creds:
    with open("google_key.json", "w") as f:
        f.write(json_creds)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("google_key.json")

PROJECT_ID = "smile-ai-486910" #

# --- SYSTEM INSTRUCTION ---
SYSTEM_INSTRUCTION = """
You are 'Smile Financial Solution AI', an elite financial advisor developed by 'Smile Financial Solution Company'.
You never mention Google or Gemini. You provide expert help in Business Planning and Financial Support.
Greet the user as a proud representative of Smile Financial Solution.
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Smile Financial AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://accounts.google.com/gsi/client" async defer></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&display=swap');
        body { background: #f8fafd; font-family: 'Google Sans', sans-serif; height: 100vh; display: flex; flex-direction: column; overflow: hidden; margin: 0; }
        
        /* Header Fix */
        .glass-header { background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); border-bottom: 1px solid #eef0f2; }
        .visit-btn { background: #e8f0fe; color: #1a73e8; border-radius: 20px; padding: 6px 16px; font-weight: 500; transition: 0.3s; }
        .visit-btn:hover { background: #d2e3fc; }

        /* Chat Layout */
        #chat-scroller { flex: 1; overflow-y: auto; padding-bottom: 20px; }
        .gemini-pill { background: white; border: 1px solid #dadce0; padding: 10px 18px; border-radius: 24px; font-size: 14px; cursor: pointer; transition: 0.2s; white-space: nowrap; }
        .gemini-pill:hover { background: #f1f3f4; border-color: #bdc1c6; }

        /* Professional Input Box */
        .bottom-container { padding: 10px 16px env(safe-area-inset-bottom); background: white; border-top: 1px solid #f1f1f1; }
        .gemini-input-bar { background: #f0f4f9; border-radius: 32px; padding: 8px 16px; display: flex; align-items: center; gap: 12px; max-width: 800px; margin: 0 auto; }
        .gemini-input-bar input { flex: 1; background: transparent; border: none; outline: none; font-size: 16px; padding: 8px 0; }
        
        .action-icon { color: #5f6368; font-size: 20px; cursor: pointer; padding: 8px; border-radius: 50%; transition: 0.2s; }
        .action-icon:hover { background: #e1e5ea; }
        
        .send-btn-active { color: #1a73e8 !important; }
        .user-msg { background: #e9eef6; border-radius: 18px; padding: 12px 18px; margin-bottom: 16px; align-self: flex-end; max-width: 85%; }
        .ai-msg-container { display: flex; gap: 12px; margin-bottom: 24px; }
        .ai-logo-circle { width: 32px; height: 32px; background: #1a73e8; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="flex-1 flex flex-col justify-center items-center bg-white p-6 text-center">
        <div class="w-24 h-24 bg-blue-600 rounded-[2rem] flex items-center justify-center text-white text-5xl font-bold mb-8 shadow-lg">S</div>
        <h1 class="text-3xl font-bold text-gray-900">Smile Financial <span class="text-blue-600">AI</span></h1>
        <p class="text-gray-500 mt-4 mb-12">नमस्ते! Smile Financial Solution AI में आपका स्वागत है।<br>बिना पासवर्ड के सुरक्षित लॉगिन करें।</p>
        
        <div id="g_id_onload" data-client_id="434178553524-ebqcdglqghl6op8jj92i0vtqgpnj7uku.apps.googleusercontent.com" data-callback="onSignIn"></div>
        <div class="g_id_signin" data-type="standard" data-shape="pill" data-size="large"></div>
    </div>
    {% else %}

    <header class="glass-header p-4 flex justify-between items-center sticky top-0 z-10">
        <div class="flex items-center gap-3">
            <i class="fa-solid fa-bars text-gray-600 text-xl"></i>
            <span class="text-xl font-medium text-gray-800">Smile AI</span>
        </div>
        <div class="flex items-center gap-4">
            <a href="https://smilefinancial.in" target="_blank" class="visit-btn">Visit Site</a>
            <div class="w-9 h-9 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">M</div>
        </div>
    </header>

    <main id="chat-scroller" class="p-5">
        <div id="welcome-ui">
            <h1 class="text-4xl font-normal text-gray-800 leading-tight mt-10">नमस्ते Mohmmad<br><span class="text-gray-400">मैं Smile Financial AI हूँ, क्या सहायता करूँ?</span></h1>
            
            <div class="flex gap-3 mt-12 overflow-x-auto no-scrollbar py-2">
                <button onclick="autoAsk('एक Business Plan बनाओ')" class="gemini-pill">📊 Business Plan</button>
                <button onclick="autoAsk('Financial Support की जानकारी दो')" class="gemini-pill">💰 Financial Support</button>
                <button onclick="autoAsk('एक Professional Image बनाओ')" class="gemini-pill">🖼️ Create Image</button>
            </div>
        </div>
        <div id="conversation" class="flex flex-col mt-6"></div>
    </main>

    <div class="bottom-container">
        <div class="gemini-input-bar">
            <label for="file-picker" class="action-icon"><i class="fa-solid fa-plus"></i></label>
            <input type="file" id="file-picker" class="hidden" onchange="alert('File upload feature coming soon!')">
            
            <input type="text" id="query-input" placeholder="Smile AI से पूछें..." autocomplete="off">
            
            <i class="fa-solid fa-microphone action-icon" id="mic-btn" onclick="alert('Mic activated')"></i>
            
            <button id="send-btn" class="hidden" onclick="handleSend()">
                <i class="fa-solid fa-paper-plane action-icon send-btn-active"></i>
            </button>
        </div>
        <p class="text-[10px] text-center text-gray-400 mt-3">SMILE FINANCIAL SOLUTION COMPANY © 2026</p>
    </div>

    {% endif %}

    <script>
        function onSignIn(resp) {
            fetch('/login-sync', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({token: resp.credential})
            }).then(() => window.location.reload());
        }

        const qInput = document.getElementById('query-input');
        const sBtn = document.getElementById('send-btn');
        const mBtn = document.getElementById('mic-btn');

        qInput?.addEventListener('input', () => {
            const hasText = qInput.value.trim() !== "";
            sBtn.classList.toggle('hidden', !hasText);
            mBtn.classList.toggle('hidden', hasText);
        });

        async function handleSend() {
            const text = qInput.value.trim();
            if(!text) return;
            
            document.getElementById('welcome-ui').style.display = 'none';
            const chat = document.getElementById('conversation');
            
            // User UI
            chat.innerHTML += `<div class="user-msg">${text}</div>`;
            qInput.value = "";
            sBtn.classList.add('hidden');
            mBtn.classList.remove('hidden');

            const aiId = "ai-" + Date.now();
            chat.innerHTML += `
                <div class="ai-msg-container" id="${aiId}">
                    <div class="ai-logo-circle">S</div>
                    <div class="flex flex-col">
                        <span class="text-blue-500 text-xs font-bold animate-pulse mb-1">Smile AI is thinking...</span>
                        <div class="text-gray-400">...</div>
                    </div>
                </div>`;
            
            const scroller = document.getElementById('chat-scroller');
            scroller.scrollTop = scroller.scrollHeight;

            const res = await fetch('/ask-ai', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: text})
            });
            const data = await res.json();
            
            document.getElementById(aiId).innerHTML = `
                <div class="ai-logo-circle">S</div>
                <div class="text-gray-800 leading-relaxed">${data.reply}</div>`;
            scroller.scrollTop = scroller.scrollHeight;
        }

        function autoAsk(val) { qInput.value = val; handleSend(); }
    </script>
</body>
</html>
