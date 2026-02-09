import requests
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "smile_fin_premium_key_99" # Security for login sessions

# Demo User Details
USERS = {"test@example.com": "password123"}

# --- FULL BRANDED INTERFACE (Login + Dashboard) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, interactive-widget=resizes-content">
    <title>Smile AI - Professional Workspace</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --vh: 1vh; }
        body { background: #030508; color: #e5e7eb; font-family: 'Inter', sans-serif; height: calc(var(--vh) * 100); overflow: hidden; }
        .sidebar { background: #0d1117; width: 260px; border-right: 1px solid #1a1a1a; transition: 0.3s; }
        .ai-glow { text-shadow: 0 0 10px #00f2fe; color: #00f2fe; }
        .glass-card { background: rgba(22, 27, 34, 0.8); border: 1px solid #30363d; border-radius: 15px; }
        .input-container { background: #161b22; border: 1px solid #30363d; border-radius: 24px; padding: 8px 16px; width: 90%; max-width: 800px; margin: 0 auto 20px auto; }
        @media (max-width: 768px) { .sidebar { display: none; } }
    </style>
</head>
<body class="flex flex-col md:flex-row">

    {% if not logged_in %}
    <div class="flex-1 flex flex-col justify-center items-center p-6">
        <h1 class="text-4xl font-black ai-glow mb-2">SMILE <span class="text-white">AI</span></h1>
        <p class="text-gray-500 mb-8 font-medium">Branded Financial Workspace</p>
        <form method="POST" action="/" class="bg-[#0d1117] p-8 rounded-3xl border border-[#30363d] w-full max-w-sm shadow-2xl">
            <div class="mb-4">
                <label class="block text-xs font-bold text-gray-400 mb-2 uppercase">Email Address</label>
                <input type="email" name="email" required class="w-full bg-[#030508] border border-[#30363d] rounded-xl p-3 outline-none focus:border-blue-500 transition">
            </div>
            <div class="mb-6">
                <label class="block text-xs font-bold text-gray-400 mb-2 uppercase">Password</label>
                <input type="password" name="password" required class="w-full bg-[#030508] border border-[#30363d] rounded-xl p-3 outline-none focus:border-blue-500 transition">
            </div>
            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl transition">LOG IN</button>
            <p class="text-center text-[10px] text-gray-600 mt-4">Demo: test@example.com / password123</p>
        </form>
    </div>

    {% else %}
    <aside class="sidebar hidden md:flex flex-col p-4">
        <div class="mb-10">
            <h1 class="text-xl font-black ai-glow">SMILE <span class="text-white text-sm">PRO</span></h1>
        </div>
        <nav class="flex-1 space-y-2">
            <p class="text-gray-500 text-[10px] font-bold uppercase tracking-widest px-2 mb-4">My Stuff</p>
            <button class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-gray-800 transition text-sm text-gray-300">
                <i class="fa-solid fa-plus text-blue-400"></i> New Chat
            </button>
            <button class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-gray-800 transition text-sm text-gray-300">
                <i class="fa-solid fa-gem text-purple-400"></i> Gems
            </button>
            <button class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-gray-800 transition text-sm text-gray-300">
                <i class="fa-solid fa-clock-rotate-left text-gray-400"></i> History
            </button>
        </nav>
        <div class="border-t border-gray-800 pt-4">
            <a href="/logout" class="flex items-center gap-3 p-3 text-red-400 text-sm hover:bg-red-900/10 rounded-xl">
                <i class="fa-solid fa-right-from-bracket"></i> Logout
            </a>
        </div>
    </aside>

    <main class="flex-1 flex flex-col relative h-full">
        <header class="flex justify-between items-center p-4 border-b border-[#1a1a1a]">
            <div class="md:hidden text-blue-400"><i class="fa-solid fa-bars-staggered"></i></div>
            <div class="hidden md:block text-gray-400 text-xs">Model: Smile-GPT-5 (V2)</div>
            <a href="https://smilefinancialsolution.com/" class="bg-gray-800 px-4 py-1.5 rounded-full text-[10px] font-bold border border-gray-700">Visit Website</a>
        </header>

        <div id="chat-content" class="flex-1 overflow-y-auto p-4 md:p-8 space-y-6">
            <div class="max-w-3xl mx-auto">
                <div class="flex gap-4 mb-8">
                    <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-xs"><i class="fa-solid fa-robot"></i></div>
                    <div class="flex-1 space-y-2">
                        <p class="text-sm leading-relaxed text-gray-200 bg-[#0d1117] p-4 rounded-2xl border border-gray-800">
                            Namaste! Main Smile Financial AI hoon. Aapki Loan, Marketing ya Website design mein kaise madad kar sakta hoon?
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <div class="input-container flex items-center gap-3 shadow-2xl">
            <label class="cursor-pointer text-gray-400 hover:text-blue-400 transition ml-2">
                <i class="fa-solid fa-circle-plus text-xl"></i>
                <input type="file" class="hidden">
            </label>
            <input type="text" id="user-input" placeholder="Ask Smile AI or upload file..." class="flex-1 bg-transparent outline-none text-sm py-2">
            <button class="text-gray-400 hover:text-blue-400 px-2"><i class="fa-solid fa-microphone text-lg"></i></button>
            <button onclick="sendMsg()" class="bg-white text-black w-8 h-8 rounded-full flex items-center justify-center hover:bg-blue-400 transition">
                <i class="fa-solid fa-arrow-up text-xs"></i>
            </button>
        </div>
    </main>
    {% endif %}

    <script>
        // Set height for mobile
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);

        async function sendMsg() {
            const input = document.getElementById('user-input');
            const chat = document.getElementById('chat-content');
            if(!input.value) return;

            const text = input.value;
            chat.innerHTML += `<div class="max-w-3xl mx-auto flex justify-end mb-4"><div class="bg-blue-600 text-white p-3 px-5 rounded-2xl text-sm shadow-lg">${text}</div></div>`;
            input.value = "";
            chat.scrollTop = chat.scrollHeight;

            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: text})
            });
            const data = await res.json();
            
            chat.innerHTML += `
                <div class="max-w-3xl mx-auto flex gap-4 mb-8">
                    <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-xs"><i class="fa-solid fa-robot"></i></div>
                    <div class="flex-1 p-4 rounded-2xl border border-gray-800 text-sm leading-relaxed bg-[#0d1117]">${data.reply}</div>
                </div>`;
            chat.scrollTop = chat.scrollHeight;

            const speech = new SpeechSynthesisUtterance(data.reply);
            speech.rate = 0.95;
            window.speechSynthesis.speak(speech);
        }
    </script>
</body>
</html>
"""

# --- BACKEND ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
        pw = request.form.get('password')
        if email in USERS and USERS[email] == pw:
            session['logged_in'] = True
            return redirect(url_for('home'))
        return "Invalid! <a href='/'>Try again</a>"
    
    return render_template_string(HTML_TEMPLATE, logged_in=session.get('logged_in'))

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    q = data.get('query', "")
    api_key = "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"
    
    system_prompt = (
        "You are an expert AI for Smile Financial Solution. Website: https://smilefinancialsolution.com/. "
        "Services: Loans, Business/Marketing Support, Web Design, AI/App Development. Contact: 7290977231. "
        "Instructions: Reply in natural human tone (English/Hindi). Be professional and concise."
    )

    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", 
            headers={"Authorization": f"Bearer {api_key}"}, 
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": q}],
                "temperature": 0.5
            })
        reply = r.json()['choices'][0]['message']['content']
    except:
        reply = "Kshama karein, connection issue hai. Please 7290977231 par contact karein."

    return jsonify({"reply": reply})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
