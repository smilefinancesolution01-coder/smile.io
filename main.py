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
    <title>Smile AI - Final</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --vh: 1vh; }
        body { 
            background: #030508; color: #f0f0f0; font-family: 'Inter', sans-serif; 
            height: calc(var(--vh) * 100); display: flex; flex-direction: column; overflow: hidden;
        }
        .ai-glow { text-shadow: 0 0 10px #00f2fe; color: #00f2fe; }
        .chat-container { flex: 1; overflow-y: auto; padding: 15px; padding-bottom: 90px; }
        .glass-card { background: rgba(20, 25, 35, 0.95); border: 1px solid #333; border-radius: 18px; margin-bottom: 12px; position: relative; }
        .input-area { position: fixed; bottom: 0; left: 0; right: 0; background: #030508; padding: 12px; border-top: 1px solid #222; }
        .wa-small { position: absolute; bottom: 8px; right: 12px; color: #2ecc71; font-size: 18px; }
    </style>
</head>
<body>
    <header class="flex justify-between items-center p-4 border-b border-gray-900 bg-[#030508] z-30">
        <h1 class="text-xl font-black ai-glow">SMILE <span class="text-white">AI</span></h1>
        <a href="https://smilefinancialsolution.com/" target="_blank" class="bg-blue-600 px-4 py-2 rounded-full text-[10px] font-bold uppercase">Visit Site</a>
    </header>

    <div id="chat-box" class="chat-container">
        <div class="glass-card p-4 max-w-[90%] border-l-4 border-blue-500 text-sm shadow-xl">
            Namaste! Main Smile Financial AI hoon. Main aapki Loan, Business Marketing, ya Tech Development mein kaise madad kar sakta hoon?
            <a href="https://wa.me/917290977231" target="_blank" class="wa-small"><i class="fa-brands fa-whatsapp"></i></a>
        </div>
    </div>

    <div class="input-area">
        <div class="flex items-center gap-2 bg-gray-900 rounded-full p-1 border border-gray-800">
            <input type="text" id="user-input" placeholder="Type or Speak..." class="flex-1 bg-transparent outline-none px-4 text-sm py-3">
            <button id="mic-btn" onclick="toggleMic()" class="w-10 h-10 rounded-full text-blue-400 flex items-center justify-center">
                <i id="mic-icon" class="fa-solid fa-microphone"></i>
            </button>
            <button onclick="sendMsg(true)" class="w-10 h-10 bg-blue-600 rounded-full text-white flex items-center justify-center">
                <i class="fa-solid fa-arrow-up text-xs"></i>
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
            recognition.lang = 'hi-IN'; // Default starts with Hindi support

            recognition.onresult = (e) => {
                const transcript = e.results[0][0].transcript;
                document.getElementById('user-input').value = transcript;
                sendMsg(false); // False means don't speak the response if text input was used (auto-voice only for mic)
            };
            recognition.onend = () => { isListening = false; document.getElementById('mic-icon').className='fa-solid fa-microphone'; };
        }

        function toggleMic() {
            if (isListening) { recognition.stop(); synth.cancel(); }
            else { synth.cancel(); recognition.start(); isListening = true; document.getElementById('mic-icon').className='fa-solid fa-stop text-red-500'; }
        }

        async function sendMsg(isManualText) {
            const input = document.getElementById('user-input');
            const chat = document.getElementById('chat-box');
            if(!input.value) return;

            const text = input.value;
            chat.innerHTML += `<div class="ml-auto bg-gray-800 p-3 rounded-2xl max-w-[80%] text-right text-xs mb-4">${text}</div>`;
            input.value = "";
            chat.scrollTop = chat.scrollHeight;

            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: text})
            });
            const data = await res.json();
            
            chat.innerHTML += `<div class="glass-card p-4 max-w-[85%] border-l-4 border-blue-400 text-sm mb-4">${data.reply}</div>`;
            chat.scrollTop = chat.scrollHeight;

            // Voice only if it was a mic input or explicitly needed
            if(!isManualText || isListening) {
                const utterance = new SpeechSynthesisUtterance(data.reply);
                utterance.lang = data.lang === 'en' ? 'en-US' : 'hi-IN';
                utterance.rate = 0.95;
                synth.speak(utterance);
            }
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
    
    # Detected English or Hindi based on query
    is_english = any(word in q.lower() for word in ["hello", "how", "what", "loan", "price", "website"])

    system_prompt = (
        "You are a human expert from Smile Financial Solution. "
        "Identity: Created by Smile Financial Solution. We provide: Financial Support, Business/Marketing Support, Website/App Development, AI Courses. "
        "Contact: Website: https://smilefinancialsolution.com/, Email: smilefinancesolution01@gmail.com, WhatsApp: 7290977231, Helpline: 8929208628. "
        "Rules: If user speaks English, reply in English. If Hindi, reply in Hindi. "
        "Tone: Natural human tone. Short answers. No bakchodi. Provide contact details only when asked."
    )

    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", 
            headers={"Authorization": f"Bearer {api_key}"}, 
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": q}],
                "temperature": 0.5,
                "max_tokens": 120
            })
        reply = r.json()['choices'][0]['message']['content']
    except:
        reply = "Kshama karein, main connect nahi kar pa raha hoon."

    return jsonify({"reply": reply, "lang": "en" if is_english else "hi"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
