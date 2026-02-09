import requests
from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, interactive-widget=resizes-content">
    <title>Smile AI - Professional</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --vh: 1vh; }
        body { 
            background: #030508; 
            color: #f0f0f0; 
            font-family: 'Inter', sans-serif; 
            height: 100vh; /* Fallback */
            height: calc(var(--vh) * 100);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .ai-glow { text-shadow: 0 0 10px #00f2fe; color: #00f2fe; }
        .chat-container { flex: 1; overflow-y: auto; padding: 15px; padding-bottom: 100px; }
        .glass-card { background: rgba(20, 25, 35, 0.95); border: 1px solid #333; border-radius: 20px; margin-bottom: 12px; }
        .input-area { 
            position: fixed; bottom: 0; left: 0; right: 0; 
            background: #030508; padding: 15px; border-top: 1px solid #222;
        }
    </style>
</head>
<body>
    <header class="flex justify-between items-center p-4 border-b border-gray-900 bg-[#030508] z-10">
        <h1 class="text-xl font-black ai-glow">SMILE <span class="text-white">AI</span></h1>
        <a href="https://smilefinancesolution.com" target="_blank" class="bg-blue-600 px-5 py-2 rounded-full text-xs font-bold uppercase shadow-lg shadow-blue-900/20">Visit Site</a>
    </header>

    <div id="chat-box" class="chat-container">
        <div class="glass-card p-4 max-w-[90%] border-l-4 border-blue-500">
            Namaste! Main Smile Financial AI hoon. Aapki loan, marketing ya website development mein kaise madad kar sakta hoon?
        </div>
    </div>

    <div class="input-area">
        <div id="call-box" class="hidden mb-3">
             <a href="tel:7290977231" class="w-full bg-green-600 py-3 rounded-xl flex justify-center items-center gap-2 font-bold text-sm">
                <i class="fa-solid fa-phone"></i> CALL EXPERT
             </a>
        </div>
        <div class="flex items-center gap-2 bg-gray-900 rounded-full p-1 border border-gray-800">
            <input type="text" id="user-input" placeholder="Bol kar ya likh kar pucho..." class="flex-1 bg-transparent outline-none px-4 text-sm py-3">
            <button id="mic-btn" onclick="toggleMic()" class="w-10 h-10 rounded-full text-blue-400 flex items-center justify-center">
                <i id="mic-icon" class="fa-solid fa-microphone"></i>
            </button>
            <button onclick="sendMsg()" class="w-10 h-10 bg-blue-600 rounded-full text-white flex items-center justify-center">
                <i class="fa-solid fa-arrow-up text-xs"></i>
            </button>
        </div>
    </div>

    <script>
        // Fix for mobile height
        const setHeight = () => {
            document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
        };
        window.addEventListener('resize', setHeight);
        setHeight();

        let isListening = false;
        let recognition;
        const synth = window.speechSynthesis;

        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
            recognition.lang = 'hi-IN';
            recognition.onresult = (e) => {
                document.getElementById('user-input').value = e.results[0][0].transcript;
                sendMsg();
            };
            recognition.onend = () => { isListening = false; document.getElementById('mic-icon').className='fa-solid fa-microphone'; };
        }

        function toggleMic() {
            if (isListening) { recognition.stop(); synth.cancel(); }
            else { recognition.start(); isListening = true; document.getElementById('mic-icon').className='fa-solid fa-stop text-red-500'; }
        }

        async function sendMsg() {
            const input = document.getElementById('user-input');
            const chat = document.getElementById('chat-box');
            if(!input.value) return;

            const text = input.value;
            chat.innerHTML += `<div class="ml-auto bg-blue-900/30 p-4 rounded-2xl max-w-[85%] text-right border-r-2 border-blue-500 text-sm mb-4">${text}</div>`;
            input.value = "";
            chat.scrollTop = chat.scrollHeight;

            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: text})
            });
            const data = await res.json();
            
            chat.innerHTML += `<div class="glass-card p-4 max-w-[85%] border-l-4 border-blue-400 text-sm mb-4">${data.reply}</div>`;
            if(data.call_logic) document.getElementById('call-box').classList.remove('hidden');
            chat.scrollTop = chat.scrollHeight;

            const utterance = new SpeechSynthesisUtterance(data.reply);
            utterance.rate = 0.9;
            synth.speak(utterance);
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
    q = data.get('query', "")
    api_key = "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"
    
    system_prompt = (
        "Role: Human Expert from Smile Financial Solution. "
        "Contact: Helpline/WhatsApp 7290977231, Mail: info@smilefinancesolution.com. "
        "Services: Financial Support (Loans), Business Support, Marketing Support, Website Design, AI Courses, AI & App Development. "
        "Identity: Created by Smile Financial Solution. We operate Pan India, generate employment, and have 10,000+ success stories. "
        "Instructions: Reply instantly, be natural (not like AI), and keep it concise. If they ask about services or contact, provide the details immediately."
    )

    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", 
            headers={"Authorization": f"Bearer {api_key}"}, 
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": q}],
                "temperature": 0.6
            })
        reply = r.json()['choices'][0]['message']['content']
    except:
        reply = "Kshama karein, main abhi connect nahi kar pa raha. Please 7290977231 par sampark karein."

    return jsonify({"reply": reply, "call_logic": True if "call" in q.lower() or "contact" in q.lower() else False})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
