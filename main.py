import requests
from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# FINAL PRO HTML (Chat + Voice + Camera + Green Call Logic)
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Smile Financial GPT-5</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #05070a; color: #e5e7eb; font-family: 'Inter', sans-serif; overflow: hidden; }
        .glass { background: rgba(13, 17, 23, 0.8); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); }
        .ai-text { background: linear-gradient(90deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
        .glow-btn { box-shadow: 0 0 15px rgba(79, 172, 254, 0.4); transition: 0.3s; }
        .glow-btn:hover { box-shadow: 0 0 25px rgba(79, 172, 254, 0.8); transform: scale(1.05); }
    </style>
</head>
<body class="h-screen flex flex-col justify-between p-4">
    <header class="flex justify-between items-center p-2">
        <div class="flex items-center gap-2">
            <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <h1 class="text-lg font-bold tracking-tighter">SMILE <span class="ai-text">GPT-5</span></h1>
        </div>
        <button onclick="location.reload()" class="text-gray-400"><i class="fa-solid fa-rotate-right"></i></button>
    </header>

    <main id="chat-box" class="flex-1 overflow-y-auto space-y-4 p-2 text-sm md:text-base">
        <div class="glass p-4 rounded-2xl max-w-[85%] border-l-4 border-blue-500">
            Hello! I am your Smile Financial AI. How can I assist you with loans or services today?
        </div>
    </main>

    <div id="call-btn" class="hidden mb-4 animate-bounce">
        <a href="tel:7290977231" class="bg-green-600 flex items-center justify-center gap-3 p-4 rounded-2xl font-bold text-white shadow-lg">
            <i class="fa-solid fa-phone-volume text-xl"></i> CALL EXPERT NOW
        </a>
    </div>

    <footer class="space-y-4 pb-4">
        <div class="flex items-center gap-2 glass p-2 rounded-3xl border-gray-700">
            <label class="p-3 text-blue-400 cursor-pointer">
                <i class="fa-solid fa-camera text-xl"></i>
                <input type="file" accept="image/*" id="img-up" class="hidden" onchange="handleImg(this)">
            </label>
            <input type="text" id="user-input" placeholder="Ask Smile AI..." class="bg-transparent flex-1 outline-none text-white px-2">
            <button id="mic-btn" onclick="startVoice()" class="p-3 text-blue-400"><i class="fa-solid fa-microphone text-xl"></i></button>
            <button onclick="sendMsg()" class="bg-blue-600 w-12 h-12 rounded-full glow-btn flex items-center justify-center">
                <i class="fa-solid fa-paper-plane"></i>
            </button>
        </div>
    </footer>

    <script>
        async function sendMsg() {
            const input = document.getElementById('user-input');
            const chat = document.getElementById('chat-box');
            if(!input.value) return;

            const userText = input.value;
            chat.innerHTML += `<div class="ml-auto glass p-4 rounded-2xl max-w-[85%] border-r-4 border-gray-500">${userText}</div>`;
            input.value = "";
            chat.scrollTop = chat.scrollHeight;

            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: userText})
            });
            const data = await res.json();
            
            chat.innerHTML += `<div class="glass p-4 rounded-2xl max-w-[85%] border-l-4 border-blue-500">${data.reply}</div>`;
            if(data.call_logic) document.getElementById('call-btn').classList.remove('hidden');
            
            const speech = new SpeechSynthesisUtterance(data.reply);
            window.speechSynthesis.speak(speech);
            chat.scrollTop = chat.scrollHeight;
        }

        function startVoice() {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.onresult = (e) => {
                document.getElementById('user-input').value = e.results[0][0].transcript;
                sendMsg();
            };
            recognition.start();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    q = data.get('query', "").lower()
    # Groq API Key
    api_key = "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"
    
    # Simple logic for call button
    needs_call = any(x in q for x in ["loan", "service", "free", "help", "mufat"])
    
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", 
            headers={"Authorization": f"Bearer {api_key}"}, 
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": "You are Smile Financial AI. Be professional."}, {"role": "user", "content": q}]
            })
        reply = r.json()['choices'][0]['message']['content']
    except:
        reply = "I am having trouble connecting. Please call 7290977231."

    return jsonify({"reply": reply, "call_logic": needs_call})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
