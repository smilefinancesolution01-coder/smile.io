import requests
from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# Full Knowledge & Human UI
HTML_CODE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Smile AI - Human Edge</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: #030508; color: #f0f0f0; font-family: 'Segoe UI', Roboto, sans-serif; overflow: hidden; }
        .ai-glow { text-shadow: 0 0 10px #00f2fe; color: #00f2fe; }
        .human-card { background: rgba(15, 20, 28, 0.9); border: 1px solid #222; border-radius: 25px; }
        .mic-active { background: #ff4b2b !important; animation: pulse 1s infinite; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255, 75, 43, 0.7); } 70% { box-shadow: 0 0 0 15px rgba(255, 75, 43, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 75, 43, 0); } }
    </style>
</head>
<body class="h-screen flex flex-col p-4">
    <header class="flex justify-between items-center mb-4">
        <div class="flex items-center gap-2">
            <h1 class="text-xl font-black ai-glow">SMILE <span class="text-white">AI</span></h1>
        </div>
        <a href="https://smilefinancesolution.com" target="_blank" class="bg-blue-600 px-4 py-2 rounded-full text-xs font-bold uppercase tracking-widest">Visit Site</a>
    </header>

    <div id="chat-box" class="flex-1 overflow-y-auto space-y-4 pb-20 custom-scroll">
        <div class="human-card p-4 max-w-[90%] border-l-4 border-blue-500">
            Namaste! Main Smile Financial AI hoon. Loan, Marketing, ya Tech development—aapko kis cheez mein help chahiye?
        </div>
    </div>

    <div class="fixed bottom-6 left-0 right-0 px-6 space-y-4">
        <div id="call-area" class="hidden">
             <a href="tel:7290977231" class="w-full bg-green-600 py-4 rounded-2xl flex justify-center items-center gap-3 font-bold shadow-2xl">
                <i class="fa-solid fa-phone-flip"></i> CALL EXPERT NOW
             </a>
        </div>

        <div class="flex items-center gap-3 bg-gray-900/80 backdrop-blur-xl p-2 rounded-full border border-gray-700 shadow-2xl">
            <input type="text" id="user-input" placeholder="Bol kar ya likh kar pucho..." class="flex-1 bg-transparent border-none outline-none px-4 text-sm">
            <button id="mic-btn" onclick="toggleMic()" class="w-12 h-12 bg-gray-800 rounded-full text-blue-400 flex items-center justify-center transition-all">
                <i id="mic-icon" class="fa-solid fa-microphone"></i>
            </button>
            <button onclick="sendMsg()" class="w-12 h-12 bg-blue-600 rounded-full text-white flex items-center justify-center">
                <i class="fa-solid fa-arrow-up"></i>
            </button>
        </div>
    </div>

    <script>
        let isListening = false;
        let recognition;
        const synth = window.speechSynthesis;

        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'hi-IN'; // Default language

            recognition.onresult = (e) => {
                const text = e.results[0][0].transcript;
                document.getElementById('user-input').value = text;
                sendMsg();
            };
            recognition.onend = () => { stopMicStyle(); };
        }

        function toggleMic() {
            if (isListening) {
                recognition.stop();
                synth.cancel(); // Turant bolna band karega
                stopMicStyle();
            } else {
                synth.cancel();
                recognition.start();
                startMicStyle();
            }
        }

        function startMicStyle() {
            isListening = true;
            document.getElementById('mic-btn').classList.add('mic-active');
            document.getElementById('mic-icon').className = 'fa-solid fa-stop';
        }

        function stopMicStyle() {
            isListening = false;
            document.getElementById('mic-btn').classList.remove('mic-active');
            document.getElementById('mic-icon').className = 'fa-solid fa-microphone';
        }

        async function sendMsg() {
            const input = document.getElementById('user-input');
            const chat = document.getElementById('chat-box');
            if(!input.value) return;

            const userText = input.value;
            chat.innerHTML += `<div class="ml-auto bg-gray-800 p-4 rounded-2xl max-w-[85%] text-right border-b-2 border-blue-500">${userText}</div>`;
            input.value = "";
            chat.scrollTop = chat.scrollHeight;

            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: userText})
            });
            const data = await res.json();
            
            chat.innerHTML += `<div class="human-card p-4 max-w-[85%] border-l-4 border-blue-400 animation-fade">${data.reply}</div>`;
            if(data.call_logic) document.getElementById('call-area').classList.remove('hidden');
            chat.scrollTop = chat.scrollHeight;

            // HUMAN VOICE SETTINGS
            const utterance = new SpeechSynthesisUtterance(data.reply);
            const voices = synth.getVoices();
            // Sabse achhi natural voice dhundne ki koshish
            utterance.voice = voices.find(v => v.name.includes('Google') || v.lang.includes('hi')) || voices[0];
            utterance.pitch = 0.9; // Thodi bhari aur human voice
            utterance.rate = 0.95; // Aram se baat karega
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
    
    # SYSTEM PROMPT: AI ko Smile Financial ki puri knowledge dena
    system_prompt = (
        "You are a human-like expert from Smile Financial Solution. "
        "Company Profile: We provide Financial, Business, and Marketing support, Website design, AI Courses, AI & App Development. "
        "We serve Pan India and generate employment. Success stories involve helping 10,000+ businesses grow. "
        "Rules: Speak in a natural human tone (Hinglish/Local language). Keep it short and to the point. No 'AI' talk. "
        "If they ask for free service or loans, suggest calling 7290977231."
    )

    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", 
            headers={"Authorization": f"Bearer {api_key}"}, 
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": q}
                ],
                "temperature": 0.5,
                "max_tokens": 150 # Short and sweet response
            })
        reply = r.json()['choices'][0]['message']['content']
    except:
        reply = "Aapka connection slow hai, please 7290977231 par call karein."

    needs_call = any(word in q.lower() for word in ["loan", "free", "service", "help", "contact"])
    return jsonify({"reply": reply, "call_logic": needs_call})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
