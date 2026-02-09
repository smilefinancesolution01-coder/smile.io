import requests
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "smile_pro_google_auth_key"

# --- BRANDED INTERFACE WITH GOOGLE LOGIN ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, interactive-widget=resizes-content">
    <title>Smile AI - Google Workspace</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://accounts.google.com/gsi/client" async defer></script>
    <style>
        :root { --vh: 1vh; }
        body { background: #030508; color: #e5e7eb; font-family: 'Inter', sans-serif; height: calc(var(--vh) * 100); overflow: hidden; }
        .sidebar { background: #0d1117; width: 260px; border-right: 1px solid #1a1a1a; transition: transform 0.3s ease; }
        .ai-glow { text-shadow: 0 0 10px #00f2fe; color: #00f2fe; }
        .input-container { background: #161b22; border: 1px solid #30363d; border-radius: 28px; padding: 10px 20px; width: 92%; max-width: 800px; margin: 0 auto 20px auto; }
        @media (max-width: 768px) {
            .sidebar { position: fixed; height: 100%; z-index: 50; transform: translateX(-100%); }
            .sidebar.active { transform: translateX(0); }
        }
    </style>
</head>
<body class="flex flex-col md:flex-row">

    {% if not logged_in %}
    <div class="flex-1 flex flex-col justify-center items-center p-6 text-center">
        <h1 class="text-5xl font-black ai-glow mb-2 tracking-tighter">SMILE <span class="text-white">AI</span></h1>
        <p class="text-gray-400 mb-10 font-medium">Please sign in to access your workspace</p>
        
        <div class="bg-[#0d1117] p-10 rounded-3xl border border-[#30363d] shadow-2xl w-full max-w-sm">
             <div id="g_id_onload"
                 data-client_id="YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
                 data-context="signin"
                 data-ux_mode="popup"
                 data-callback="handleCredentialResponse"
                 data-auto_prompt="false">
             </div>
             <div class="g_id_signin" data-type="standard" data-shape="pill" data-theme="filled_blue" data-text="signin_with" data-size="large" data-logo_alignment="left"></div>
             
             <form method="POST" action="/manual-login" class="mt-6 border-t border-gray-800 pt-6">
                <button type="submit" class="text-xs text-gray-500 hover:text-blue-400">Quick Demo Access (Skip Login)</button>
             </form>
        </div>
    </div>

    {% else %}
    <aside id="sideMenu" class="sidebar flex flex-col p-4">
        <div class="flex justify-between items-center mb-10 px-2">
            <h1 class="text-xl font-black ai-glow">SMILE <span class="text-white">PRO</span></h1>
            <button onclick="toggleMenu()" class="md:hidden text-gray-400"><i class="fa-solid fa-xmark text-xl"></i></button>
        </div>
        <nav class="flex-1 space-y-2">
            <button class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-gray-800 transition text-sm">
                <i class="fa-solid fa-plus text-blue-400"></i> New Chat
            </button>
            <button class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-gray-800 transition text-sm">
                <i class="fa-solid fa-gem text-purple-400"></i> Gems
            </button>
            <button class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-gray-800 transition text-sm">
                <i class="fa-solid fa-history text-gray-400"></i> My Stuff
            </button>
        </nav>
        <div class="border-t border-gray-800 pt-4">
            <a href="/logout" class="flex items-center gap-3 p-3 text-red-400 text-sm hover:bg-red-900/10 rounded-xl">
                <i class="fa-solid fa-right-from-bracket"></i> Logout
            </a>
        </div>
    </aside>

    <main class="flex-1 flex flex-col relative h-full">
        <header class="flex justify-between items-center p-4 border-b border-[#1a1a1a] bg-[#030508]">
            <button onclick="toggleMenu()" class="md:hidden text-blue-400 p-2"><i class="fa-solid fa-bars-staggered text-xl"></i></button>
            <div class="hidden md:block text-gray-500 text-[10px] font-bold uppercase tracking-widest">Workspace Online</div>
            <a href="https://smilefinancialsolution.com/" class="bg-blue-600 px-4 py-1.5 rounded-full text-[10px] font-bold">Visit Website</a>
        </header>

        <div id="chat-content" class="flex-1 overflow-y-auto p-4 md:p-8">
            <div class="max-w-3xl mx-auto space-y-6">
                <div class="flex gap-4">
                    <div class="w-9 h-9 rounded-full bg-blue-600 flex items-center justify-center text-white shadow-lg shadow-blue-900/40">
                        <i class="fa-solid fa-robot text-sm"></i>
                    </div>
                    <div class="flex-1 p-4 rounded-2xl bg-[#0d1117] border border-gray-800 text-sm leading-relaxed">
                        Namaste! Main Smile Financial AI hoon. Aapki Loan, Marketing ya Website design mein kaise madad kar sakta hoon?
                    </div>
                </div>
            </div>
        </div>

        <div class="input-container flex items-center gap-4 shadow-2xl mb-6">
            <label class="cursor-pointer text-gray-500 hover:text-blue-400 transition">
                <i class="fa-solid fa-circle-plus text-2xl"></i>
                <input type="file" class="hidden">
            </label>
            <input type="text" id="user-input" placeholder="Ask Smile AI or upload file..." class="flex-1 bg-transparent outline-none text-sm py-2">
            <button class="text-gray-500 hover:text-blue-400"><i class="fa-solid fa-microphone text-xl"></i></button>
            <button onclick="sendMsg()" class="bg-white text-black w-9 h-9 rounded-full flex items-center justify-center hover:bg-blue-400 transition">
                <i class="fa-solid fa-arrow-up text-sm"></i>
            </button>
        </div>
    </main>
    {% endif %}

    <script>
        function toggleMenu() {
            document.getElementById('sideMenu').classList.toggle('active');
        }

        async function sendMsg() {
            const input = document.getElementById('user-input');
            const chat = document.getElementById('chat-content');
            if(!input.value) return;

            const text = input.value;
            chat.innerHTML += `<div class="max-w-3xl mx-auto flex justify-end mb-6"><div class="bg-blue-600 text-white p-3 px-5 rounded-2xl text-sm shadow-md">${text}</div></div>`;
            input.value = "";
            chat.scrollTop = chat.scrollHeight;

            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: text})
            });
            const data = await res.json();
            
            chat.innerHTML += `
                <div class="max-w-3xl mx-auto flex gap-4 mb-6">
                    <div class="w-9 h-9 rounded-full bg-blue-600 flex items-center justify-center text-white"><i class="fa-solid fa-robot text-sm"></i></div>
                    <div class="flex-1 p-4 rounded-2xl bg-[#0d1117] border border-gray-800 text-sm leading-relaxed">${data.reply}</div>
                </div>`;
            chat.scrollTop = chat.scrollHeight;

            const speech = new SpeechSynthesisUtterance(data.reply);
            window.speechSynthesis.speak(speech);
        }

        // Handle Google Login Response
        function handleCredentialResponse(response) {
            // In real app, send 'response.credential' to backend to verify
            window.location.href = "/manual-login"; 
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, logged_in=session.get('logged_in'))

@app.route('/manual-login', methods=['POST', 'GET'])
def manual_login():
    session['logged_in'] = True
    return redirect(url_for('home'))

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    q = data.get('query', "")
    api_key = "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"
    
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", 
            headers={"Authorization": f"Bearer {api_key}"}, 
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": "You are Smile Financial AI expert."}, {"role": "user", "content": q}],
                "temperature": 0.5
            })
        reply = r.json()['choices'][0]['message']['content']
    except:
        reply = "Service busy, please try again."

    return jsonify({"reply": reply})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
