import requests
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
from datetime import datetime
import os
import uuid # For unique chat IDs

# Supabase setup (placeholders for now)
# pip install supabase-py
# from supabase import create_client, Client
# SUPABASE_URL = os.environ.get("SUPABASE_URL")
# SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your_strong_secret_key_here") # Change this for production

# Dummy user data for now (will be replaced by Supabase)
USERS = {
    "test@example.com": {"password": "password123", "name": "Test User"}
}

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, interactive-widget=resizes-content">
    <title>Smile AI - Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --vh: 1vh; }
        body { 
            background: #030508; color: #f0f0f0; font-family: 'Inter', sans-serif; 
            height: calc(var(--vh) * 100); display: flex; flex-direction: column; overflow: hidden;
        }
        .ai-glow { text-shadow: 0 0 10px #00f2fe; color: #00f2fe; }
        .sidebar { background: #0d1117; width: 250px; flex-shrink: 0; padding: 1rem; border-right: 1px solid #1a1a1a; display: flex; flex-direction: column; }
        .chat-area { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
        .chat-box { flex: 1; overflow-y: auto; padding: 1rem; padding-bottom: 90px; }
        .input-area { background: #030508; padding: 0.75rem; border-top: 1px solid #1a1a1a; }
        .glass-card { background: rgba(20, 25, 35, 0.95); border: 1px solid #333; border-radius: 18px; margin-bottom: 0.75rem; }
        .chat-item { padding: 0.75rem; border-radius: 10px; margin-bottom: 0.5rem; cursor: pointer; }
        .chat-item:hover { background: #1a1a1a; }
        .chat-item.active { background: #00f2fe20; border-left: 3px solid #00f2fe; }
        .mobile-header { display: none; }
        @media (max-width: 768px) {
            .sidebar { display: none; width: 0; }
            .mobile-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem; border-bottom: 1px solid #1a1a1a; background: #030508; }
            body { flex-direction: column; }
            .chat-area { width: 100%; }
        }
    </style>
</head>
<body class="md:flex">
    <div class="mobile-header">
        <button id="menu-toggle" class="text-blue-400 text-lg"><i class="fa-solid fa-bars"></i></button>
        <h1 class="text-xl font-black ai-glow ml-4">SMILE <span class="text-white">AI</span></h1>
        <a href="https://smilefinancialsolution.com/" target="_blank" class="bg-blue-600 px-3 py-1 rounded-full text-[10px] font-bold uppercase">Visit Site</a>
    </div>

    <aside id="sidebar" class="sidebar hidden md:flex">
        <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-bold ai-glow">My Workspace</h2>
            <button onclick="newChat()" class="bg-blue-600 w-8 h-8 rounded-full text-white flex items-center justify-center text-sm"><i class="fa-solid fa-plus"></i></button>
        </div>
        
        <div class="flex-1 overflow-y-auto mb-6">
            <button class="chat-item active w-full text-left" onclick="loadChat('new')">
                <i class="fa-solid fa-comment-dots mr-2"></i> New Chat
            </button>
            <div id="past-chats">
                </div>
        </div>

        <div class="mt-auto border-t border-gray-700 pt-4">
            <div class="flex items-center gap-3 mb-4">
                <img src="https://api.dicebear.com/7.x/initials/svg?seed={{user_name}}" alt="Avatar" class="w-8 h-8 rounded-full">
                <span>{{user_name}}</span>
            </div>
            <button onclick="logout()" class="w-full bg-red-600 py-2 rounded-lg text-sm font-bold">Logout</button>
        </div>
    </aside>

    <div class="chat-area">
        <header class="hidden md:flex justify-between items-center p-4 border-b border-gray-900 bg-[#030508] z-10">
            <h1 class="text-xl font-black ai-glow">SMILE <span class="text-white">AI</span></h1>
            <a href="https://smilefinancialsolution.com/" target="_blank" class="bg-blue-600 px-5 py-2 rounded-full text-xs font-bold uppercase shadow-lg shadow-blue-900/20">Visit Site</a>
        </header>

        <div id="chat-box" class="chat-box">
            <div class="glass-card p-4 max-w-[90%] border-l-4 border-blue-500 text-sm">
                Namaste {{user_name}}! Main Smile Financial AI hoon. Aapki loan, marketing, ya Tech Development mein kaise madad kar sakta hoon?
            </div>
        </div>

        <div class="input-area">
            <div class="flex items-center gap-2 bg-gray-900 rounded-full p-1 border border-gray-800 shadow-inner">
                <input type="file" id="image-upload" accept="image/*" class="hidden" onchange="previewImage(event)">
                <button onclick="document.getElementById('image-upload').click()" class="w-10 h-10 rounded-full text-green-400 flex items-center justify-center text-lg">
                    <i class="fa-solid fa-image"></i>
                </button>
                <input type="text" id="user-input" placeholder="Bol kar ya likh kar pucho..." class="flex-1 bg-transparent outline-none px-4 text-sm py-3">
                <button id="mic-btn" onclick="toggleMic()" class="w-10 h-10 rounded-full text-blue-400 flex items-center justify-center">
                    <i id="mic-icon" class="fa-solid fa-microphone"></i>
                </button>
                <button onclick="sendMsg()" class="w-10 h-10 bg-blue-600 rounded-full text-white flex items-center justify-center shadow-lg">
                    <i class="fa-solid fa-arrow-up"></i>
                </button>
            </div>
            <div id="image-preview" class="hidden flex items-center justify-between p-2 mt-2 bg-gray-800 rounded-lg">
                <img id="preview-img" class="h-10 w-10 object-cover rounded mr-2">
                <span id="image-name" class="text-xs text-gray-400 flex-1"></span>
                <button onclick="removeImage()" class="text-red-400 text-sm"><i class="fa-solid fa-times"></i></button>
            </div>
        </div>
    </div>

    <script>
        const setHeight = () => { document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`); };
        window.addEventListener('resize', setHeight);
        setHeight();

        // Mobile Sidebar Toggle
        document.getElementById('menu-toggle').addEventListener('click', () => {
            const sidebar = document.getElementById('sidebar');
            if (sidebar.classList.contains('hidden')) {
                sidebar.classList.remove('hidden');
                sidebar.classList.add('fixed', 'inset-y-0', 'left-0', 'z-40');
            } else {
                sidebar.classList.add('hidden');
                sidebar.classList.remove('fixed', 'inset-y-0', 'left-0', 'z-40');
            }
        });

        // Chat Logic
        let currentChatId = 'new'; // Default to a new chat
        let isListening = false;
        let recognition;
        const synth = window.speechSynthesis;
        let selectedImageFile = null;

        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
            recognition.lang = 'en-IN'; // Default to English for broader recognition, we'll set it dynamically later
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.onresult = (e) => {
                document.getElementById('user-input').value = e.results[0][0].transcript;
                sendMsg();
            };
            recognition.onend = () => { isListening = false; document.getElementById('mic-icon').className='fa-solid fa-microphone'; };
        }

        function toggleMic() {
            if (isListening) { recognition.stop(); synth.cancel(); }
            else { synth.cancel(); recognition.start(); isListening = true; document.getElementById('mic-icon').className='fa-solid fa-stop text-red-500'; }
        }

        function newChat() {
            currentChatId = 'new';
            document.getElementById('chat-box').innerHTML = `
                <div class="glass-card p-4 max-w-[90%] border-l-4 border-blue-500 text-sm">
                    Namaste {{user_name}}! Main Smile Financial AI hoon. Aapki kaise madad kar sakta hoon?
                </div>
            `;
            // Remove active class from old chat and add to new chat
            document.querySelectorAll('.chat-item').forEach(item => item.classList.remove('active'));
            document.querySelector('.chat-item[onclick*="new"]').classList.add('active');
            removeImage(); // Clear any pending image for new chat
        }

        // Dummy loadChat for now, will fetch from DB
        function loadChat(chatId) {
            currentChatId = chatId;
            document.getElementById('chat-box').innerHTML = `
                <div class="glass-card p-4 max-w-[90%] border-l-4 border-blue-500 text-sm">
                    Loading chat ${chatId}... (This will fetch from database later)
                </div>
            `;
            document.querySelectorAll('.chat-item').forEach(item => item.classList.remove('active'));
            document.querySelector(`.chat-item[onclick*="${chatId}"]`).classList.add('active');
            removeImage();
        }

        function previewImage(event) {
            const file = event.target.files[0];
            if (file) {
                selectedImageFile = file;
                const reader = new FileReader();
                reader.onload = (e) => {
                    document.getElementById('preview-img').src = e.target.result;
                    document.getElementById('image-name').textContent = file.name;
                    document.getElementById('image-preview').classList.remove('hidden');
                };
                reader.readAsDataURL(file);
            }
        }

        function removeImage() {
            selectedImageFile = null;
            document.getElementById('image-upload').value = '';
            document.getElementById('image-preview').classList.add('hidden');
            document.getElementById('preview-img').src = '';
            document.getElementById('image-name').textContent = '';
        }


        async function sendMsg() {
            const input = document.getElementById('user-input');
            const chat = document.getElementById('chat-box');
            if(!input.value && !selectedImageFile) return;

            const userText = input.value;
            const chatMessageId = `msg-${uuidv4()}`; // Unique ID for each message

            let userContentHTML = `<div class="ml-auto bg-blue-900/40 p-3 rounded-2xl max-w-[80%] text-right text-xs mb-4">`;
            if (userText) userContentHTML += userText;
            if (selectedImageFile) {
                userContentHTML += `<img src="${document.getElementById('preview-img').src}" class="max-w-full h-auto rounded mt-2">`;
                userContentHTML += `<span class="block text-right text-gray-500 text-xs mt-1">Image: ${selectedImageFile.name}</span>`;
            }
            userContentHTML += `</div>`;
            chat.innerHTML += userContentHTML;
            
            input.value = "";
            chat.scrollTop = chat.scrollHeight;

            const formData = new FormData();
            formData.append('query', userText);
            formData.append('chat_id', currentChatId); // Send current chat ID
            if (selectedImageFile) {
                formData.append('image', selectedImageFile);
            }
            removeImage(); // Clear image after sending

            const res = await fetch('/ask', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            
            chat.innerHTML += `<div class="glass-card p-4 max-w-[85%] border-l-4 border-blue-400 text-sm mb-4 leading-relaxed">${data.reply}</div>`;
            chat.scrollTop = chat.scrollHeight;

            const utterance = new SpeechSynthesisUtterance(data.reply);
            utterance.lang = data.lang === 'en' ? 'en-US' : 'hi-IN';
            utterance.rate = 0.95;
            synth.speak(utterance);
        }

        // Dummy UUID generator for front-end (real UUID will be from backend)
        function uuidv4() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
        }

        function logout() {
            window.location.href = '/logout'; // Redirect to backend logout endpoint
        }

        // Load past chats (dummy for now)
        function loadPastChats() {
            const pastChatsDiv = document.getElementById('past-chats');
            // Example dummy chats
            pastChatsDiv.innerHTML = `
                <button class="chat-item w-full text-left" onclick="loadChat('chat1')">
                    <i class="fa-solid fa-history mr-2"></i> Old Chat 1
                </button>
                <button class="chat-item w-full text-left" onclick="loadChat('chat2')">
                    <i class="fa-solid fa-history mr-2"></i> Old Chat 2
                </button>
            `;
        }
        loadPastChats(); // Call on load
    </script>
</body>
</html>
"""

# --- Routes for Authentication ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Dummy login check
        if email in USERS and USERS[email]['password'] == password:
            session['logged_in'] = True
            session['user_email'] = email
            session['user_name'] = USERS[email]['name']
            return redirect(url_for('dashboard'))
        return render_template_string("""
            <h1 style="color:red;">Login Failed</h1>
            <a href="/login">Try Again</a>
        """)
    return render_template_string("""
        <div style="background:#030508; color:white; height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; font-family:sans-serif;">
            <h1 style="font-size:2em; color:#00f2fe;">SMILE AI Login</h1>
            <form method="post" action="/login" style="background:#0d1117; padding:40px; border-radius:15px; border:1px solid #333; display:flex; flex-direction:column; gap:20px; width:300px;">
                <input type="email" name="email" placeholder="Email" required style="padding:10px; border-radius:5px; border:1px solid #444; background:transparent; color:white;">
                <input type="password" name="password" placeholder="Password" required style="padding:10px; border-radius:5px; border:1px solid #444; background:transparent; color:white;">
                <button type="submit" style="background:#00f2fe; color:black; padding:10px; border-radius:5px; border:none; cursor:pointer; font-weight:bold;">Login</button>
            </form>
            <p style="margin-top:20px; color:#aaa;">(Use test@example.com / password123 for demo)</p>
        </div>
    """)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_email', None)
    session.pop('user_name', None)
    return redirect(url_for('login'))

# --- Main Dashboard Route ---
@app.route('/dashboard')
def dashboard():
    # if not session.get('logged_in'):
    #     return redirect(url_for('login'))
    user_name = session.get('user_name', 'Guest') # Default to Guest if not logged in
    return render_template_string(HTML_CODE, user_name=user_name)

# --- AI Ask Route (Handles image uploads too) ---
@app.route('/ask', methods=['POST'])
def ask():
    q = request.form.get('query', "")
    image_file = request.files.get('image') # Get image file if uploaded
    chat_id = request.form.get('chat_id', 'new') # Get current chat ID

    api_key = "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"
    
    # System Prompt with full company details
    system_prompt = (
        "You are an expert AI assistant for Smile Financial Solution. "
        "Company Details: Website: https://smilefinancialsolution.com/, Email: smilefinancesolution01@gmail.com, "
        "WhatsApp: 7290977231, Contact: 8586051944, Helpline: 8929208628. "
        "Services: Financial Support (Loans, Appointments), Business Support, Marketing Support, Website Design, AI Courses, AI & App Development. "
        "Success: 10,000+ happy clients, Pan India service, generates employment. "
        "Instructions: Be a human-like, professional, and concise expert. Adapt to user's language (English/Hindi). "
        "Understand intent despite typos. Provide relevant contact info when asked about services or appointments. "
        "If an image is provided, focus on describing and answering questions about the image first. "
    )

    messages = [{"role": "system", "content": system_prompt}]

    # Handle image content for AI if available
    if image_file:
        # For actual image processing, you'd send this to a Vision API (e.g., Llama-Vision, OpenAI Vision)
        # For now, we'll just simulate a reply for the image
        q_with_image = f"User has provided an image. Their query: {q if q else 'Please describe this image.'}"
        messages.append({"role": "user", "content": q_with_image})
        # Placeholder for actual Vision API call
        reply = "Thank you for the image! Currently, I'm under development for advanced image analysis. But I can help you with text queries."
        # If you integrate a Vision API, your reply would come from there.
    elif q:
        messages.append({"role": "user", "content": q})
    else:
        return jsonify({"reply": "Please provide a query or an image.", "lang": "en"})

    try:
        # Only call Groq if no image or if we want Groq to respond after image processing
        if not image_file or q: # Call Groq if there's text query or no image
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                headers={"Authorization": f"Bearer {api_key}"}, 
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages,
                    "temperature": 0.5,
                    "max_tokens": 150
                })
            reply = r.json()['choices'][0]['message']['content']
        
        # Determine language for speech synthesis
        lang_code = "en" if any(word in q.lower() for word in ["hello", "how", "what", "loan", "website", "enquiry"]) else "hi"

    except Exception as e:
        print(f"Groq API Error: {e}")
        reply = "Kshama karein, main abhi connect nahi kar pa raha hoon. Technical issue hai, please 7290977231 par sampark karein."
        lang_code = "hi"

    return jsonify({"reply": reply, "lang": lang_code})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
