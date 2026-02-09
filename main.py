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
    <title>Smile AI - Human Mode</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --vh: 1vh; }
        body { 
            background: #030508; color: #f0f0f0; font-family: 'Inter', sans-serif; 
            height: calc(var(--vh) * 100); display: flex; flex-direction: column; overflow: hidden;
        }
        .ai-glow { text-shadow: 0 0 10px #00f2fe; color: #00f2fe; }
        .chat-container { flex: 1; overflow-y: auto; padding: 15px; padding-bottom: 120px; }
        .glass-card { background: rgba(20, 25, 35, 0.95); border: 1px solid #333; border-radius: 20px; margin-bottom: 12px; animation: fadeIn 0.3s ease; }
        .input-area { position: fixed; bottom: 0; left: 0; right: 0; background: #030508; padding: 15px; border-top: 1px solid #222; z-index: 20; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <header class="flex justify-between items-center p-4 border-b border-gray-900 bg-[#030508] z-30">
        <h1 class="text-xl font-black ai-glow tracking-tighter">SMILE <span class="text-white">AI</span></h1>
        <a href="https://smilefinancialsolution.com/" target="_blank" class="bg-blue-600 px-5 py-2 rounded-full text-xs font-bold uppercase shadow-lg shadow-blue-900/20">Visit Site</a>
    </header>

    <div id="chat-box" class="chat-container">
        <div class="glass-card p-4 max-w-[90%] border-l-4 border-blue-500 text-sm">
            Namaste! Main Smile Financial AI hoon. Main aapki Loan, Business Marketing, ya Website/App Development mein kaise madad kar sakta hoon?
        </div>
    </div>

    <div class="input-area">
        <div id="call-box" class="hidden mb-3 grid grid-cols-2 gap-2">
             <a href="tel:7290977231" class="bg-green-600 py-3 rounded-xl flex justify-center items-center gap-2 font-bold text-[10px]">
                <i class="fa-solid fa-whatsapp"></i> WHATSAPP
             </a>
             <a href="tel:8929208628" class="bg-blue-600 py-3 rounded-xl flex justify-center items-center gap-2 font-bold text-[10px]">
                <i class="fa-solid fa-phone"></i> HELPLINE
             </a>
        </div>
        <div class="flex items-center gap-2 bg-gray-900 rounded-full p-1 border border-gray-800 shadow-inner">
            <input type="text" id="user-input" placeholder="Bol kar pucho..." class="flex-1 bg-transparent outline-none px-4 text-sm py-3">
            <button id="mic-btn" onclick="toggleMic()" class="w-12 h-12 rounded-full text-blue-400 flex items-center justify-center">
                <i id="mic-icon" class="fa-solid fa-microphone text-xl"></i>
            </button>
            <button onclick="sendMsg()" class="w-12 h-12 bg-blue-600 rounded-full text-white flex items-center justify-center shadow-lg">
                <i class="fa-solid fa-arrow-up"></i>
            </button>
        </div>
    </div>

    <script>
        const setHeight = () => { document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`); };
        window.addEventListener('resize', setHeight);
        setHeight();

        let isListening = false;
        let recognition;
        const synth = window.speechSynthesis;

        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'hi-IN';

            recognition.onresult = (e) => {
                const transcript = e.results[0][0].transcript;
                document.getElementById('user-input').value = transcript;
                sendMsg();
            };
            recognition.onend = () => { stopMicUI(); };
            recognition.onerror = () => { stopMicUI(); };
        }

        function toggleMic() {
            if (isListening) { recognition.stop(); synth.cancel(); }
            else { 
                synth.cancel();
                try { recognition.start(); startMicUI(); } catch(e) { console.log(e); }
            }
        }

        function startMicUI() { isListening = true; document.getElementById('mic-icon').className='fa-solid fa-circle-stop text-red-500 animate-pulse'; }
        function stopMicUI() { isListening = false; document.getElementById('mic-icon').className='fa-solid fa-microphone'; }

        async function sendMsg() {
            const input = document.getElementById('user-input');
            const chat = document.getElementById('chat-box');
            if(!input.value) return;

            const text = input.value;
            chat.innerHTML += `<div class="ml-auto bg-blue-900/40 p-4 rounded-2xl max-w-[85%] text-right border-r-2 border-blue-400 text-sm mb-4">${text}</div>`;
            input.value = "";
            chat.scrollTop = chat.scrollHeight;

            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: text})
            });
            const data = await res.json();
            
            chat.innerHTML += `<div class="glass-card p-4 max-w-[85%] border-l-4 border-blue-400 text-sm mb-4 leading-relaxed">${data.reply}</div>`;
            if(data.call_logic) document.getElementById('call-box').classList.remove('hidden');
            chat.scrollTop = chat.scrollHeight;

            const utterance = new SpeechSynthesisUtterance(data.reply);
            utterance.rate = 0.95;
            utterance.pitch = 1;
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
    
    # Updated Knowledge Base with your provided details
    system_prompt = (
        "Role: Human Expert from Smile Financial Solution. "
        "Official Website: https://smilefinancialsolution.com/ "
        "Official Email: smilefinancesolution01@gmail.com "
        "WhatsApp: 7290977231 | Contact: 8586051944 | Helpline: 8929208628. "
        "Services: Financial Support (Loans), Business Support, Marketing Support, Website Design, AI Courses, AI & App Development. "
        "Success: 10,000+ stories, Pan India service, generates employment. "
        "Instructions: Ignore spelling mistakes in user query and understand the intent. Reply in a natural human tone, keep it short. "
        "Always provide contact info if the user looks interested in services."
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
        reply = "Kshama karein, connection slow hai. Aap 7290977231 par call ya WhatsApp kar sakte hain."

    return jsonify({"reply": reply, "call_logic": True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
