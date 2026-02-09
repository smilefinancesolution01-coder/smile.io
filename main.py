import os
import requests
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
# Gemini 3 ke liye new library (Iske liye 'pip install google-genai' karna hoga)
from google import genai 
from google.genai import types

app = Flask(__name__)
app.secret_key = "smile_pro_gemini_3_ultra"

# --- CONFIGURATION ---
# Bhai yahan apni Google Cloud Project ID daalna agar Gemini 3 use karna hai
os.environ["GOOGLE_CLOUD_PROJECT"] = "smile-ai-486910" 
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"

# --- INTERFACE (ASLI GEMINI 3 MOBILE LOOK) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Gemini 3 Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://accounts.google.com/gsi/client" async defer></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&display=swap');
        body { background: #f8fafd; color: #1f1f1f; font-family: 'Google Sans', sans-serif; height: 100vh; overflow: hidden; display: flex; flex-direction: column; }
        .gemini-pill { background: white; border: 1px solid #e0e0e0; border-radius: 24px; padding: 10px 16px; font-size: 14px; display: flex; align-items: center; gap: 8px; cursor: pointer; }
        .bottom-container { background: white; padding: 12px 16px 30px 16px; border-top: 1px solid #f0f0f0; }
        .input-wrapper { background: #f0f4f9; border-radius: 32px; padding: 10px 18px; display: flex; align-items: center; gap: 12px; }
        .sidebar { background: white; position: fixed; left: 0; top: 0; bottom: 0; width: 280px; z-index: 100; transform: translateX(-100%); transition: 0.3s ease; box-shadow: 4px 0 15px rgba(0,0,0,0.05); }
        .sidebar.active { transform: translateX(0); }
        .user-avatar { width: 32px; height: 32px; border-radius: 50%; background: #4caf50; color: white; display: flex; align-items: center; justify-content: center; font-size: 14px; }
        .thinking-step { color: #4285f4; font-size: 12px; font-style: italic; margin-bottom: 5px; display: block; }
        #chat-container::-webkit-scrollbar { width: 0px; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="flex-1 flex flex-col justify-center items-center bg-white p-6">
        <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d473530c2731a4cd0247d.svg" class="w-16 mb-6">
        <h1 class="text-3xl font-medium mb-10">Smile AI <span class="text-blue-500">3</span></h1>
        <div id="g_id_onload" data-client_id="434178553524-ebqcdglqghl6op8jj92i0vtqgpnj7uku.apps.googleusercontent.com" data-callback="handleCredentialResponse"></div>
        <div class="g_id_signin" data-type="standard" data-shape="pill"></div>
    </div>
    {% else %}

    <header class="p-4 flex justify-between items-center bg-white">
        <button onclick="toggleMenu()"><i class="fa-solid fa-bars text-xl"></i></button>
        <span class="text-xl font-medium tracking-tight">Gemini <span class="text-xs bg-blue-100 text-blue-600 px-2 rounded">3 PRO</span></span>
        <div class="user-avatar">M</div>
    </header>

    <main id="chat-container" class="flex-1 overflow-y-auto px-5">
        <div id="welcome-screen" class="mt-8">
            <h1 class="text-3xl font-normal mb-8">नमस्ते Mohmmad<br><span class="text-gray-400">मैं आपकी कैसे मदद कर सकता हूँ?</span></h1>
            <div class="flex flex-wrap gap-2">
                <div class="gemini-pill" onclick="fillInput('इमेज बनाएँ')"><span>🖼️</span> इमेज बनाएँ</div>
                <div class="gemini-pill" onclick="fillInput('C++ कोडिंग में मदद करें')"><span>💻</span> कोडिंग</div>
                <div class="gemini-pill" onclick="fillInput('मेरा दिन प्लान करें')"><span>📅</span> प्लानिंग</div>
            </div>
        </div>
        <div id="messages" class="space-y-6 pb-10 mt-4"></div>
    </main>

    <div class="bottom-container">
        <div class="input-wrapper">
            <label class="cursor-pointer text-gray-500"><i class="fa-solid fa-plus text-xl"></i><input type="file" class="hidden"></label>
            <input type="text" id="user-input" placeholder="Gemini से पूछें" class="flex-1 bg-transparent outline-none py-1">
            <i class="fa-solid fa-microphone text-xl text-gray-500" id="mic-btn"></i>
            <button onclick="sendMsg()" id="send-btn" class="hidden text-blue-600"><i class="fa-solid fa-paper-plane text-xl"></i></button>
        </div>
    </div>
    {% endif %}

    <script>
        function toggleMenu() { document.getElementById('sideMenu')?.classList.toggle('active'); }
        function fillInput(text) { document.getElementById('user-input').value = text; }

        const input = document.getElementById('user-input');
        input?.addEventListener('input', () => {
            const hasText = input.value.trim() !== "";
            document.getElementById('send-btn').classList.toggle('hidden', !hasText);
            document.getElementById('mic-btn').classList.toggle('hidden', hasText);
        });

        async function sendMsg() {
            const text = input.value;
            if(!text) return;
            document.getElementById('welcome-screen').style.display = 'none';
            document.getElementById('messages').innerHTML += `<div class="flex justify-end"><div class="bg-[#e9eef6] px-4 py-2 rounded-2xl max-w-[85%]">${text}</div></div>`;
            input.value = "";

            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: text})
            });
            const data = await res.json();
            
            document.getElementById('messages').innerHTML += `
                <div class="flex gap-3">
                    <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d473530c2731a4cd0247d.svg" class="w-6 h-6 mt-1">
                    <div>
                        <span class="thinking-step">Gemini 3 Thinking...</span>
                        <div class="text-[15px] text-gray-800">${data.reply}</div>
                    </div>
                </div>`;
            document.getElementById('chat-container').scrollTop = document.getElementById('chat-container').scrollHeight;
        }

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
    
    # GEMINI 3 INTEGRATION LOGIC
    # Bhai, agar Google Cloud set hai toh ye use karega, warna fallback Llama par jayega
    try:
        # client = genai.Client() # Gemini 3 Client
        # response = client.models.generate_content(
        #    model="gemini-3-pro-preview",
        #    contents=q,
        #    config=types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.HIGH))
        # )
        # reply = response.text
        
        # TESTING FALLBACK (Jab tak SDK install na ho):
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", 
            headers={"Authorization": f"Bearer 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"}, 
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": q}]})
        reply = r.json()['choices'][0]['message']['content']
    except:
        reply = "Gemini 3 Connection Error. Please check Project ID."

    return jsonify({"reply": reply})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
