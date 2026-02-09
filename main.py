import os
import json
from flask import Flask, request, jsonify, render_template_string, session
from google import genai
from google.genai import types

app = Flask(__name__)
app.secret_key = "smile_financial_final_fix"

# --- SERVICE ACCOUNT SETUP ---
#
json_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if json_creds:
    with open("google_key.json", "w") as f:
        f.write(json_creds)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("google_key.json")

PROJECT_ID = "smile-ai-486910" 

@app.route('/login-sync', methods=['POST'])
def login_sync():
    session['logged_in'] = True
    return jsonify({"status": "success"})

@app.route('/ask-ai', methods=['POST'])
def ask_ai():
    user_query = request.json.get('query', "")
    try:
        # Vertex AI Client Initialization
        client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_query,
            config=types.GenerateContentConfig(
                system_instruction="You are Smile Financial Solution AI, created by Smile Financial Solution Company. Be professional and never mention Google/Gemini."
            )
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Technical Error: {str(e)}"})

# UI Template with Google One-Tap & Gemini Layout
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>Smile AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://accounts.google.com/gsi/client" async defer></script>
    <style>
        body { background: #f8fafd; font-family: sans-serif; height: 100vh; display: flex; flex-direction: column; }
        .gemini-input-bar { background: #f0f4f9; border-radius: 32px; padding: 12px 20px; display: flex; align-items: center; gap: 12px; }
        .user-msg { background: #e9eef6; border-radius: 18px; padding: 12px; margin-bottom: 10px; align-self: flex-end; }
    </style>
</head>
<body>
    {% if not logged_in %}
    <div class="flex-1 flex flex-col justify-center items-center bg-white p-6">
        <div class="w-20 h-20 bg-blue-600 rounded-3xl flex items-center justify-center text-white text-4xl font-bold mb-6">S</div>
        <h1 class="text-3xl font-bold mb-10">Smile Financial AI</h1>
        <div id="g_id_onload" data-client_id="434178553524-ebqcdglqghl6op8jj92i0vtqgpnj7uku.apps.googleusercontent.com" data-callback="onSignIn"></div>
        <div class="g_id_signin" data-type="standard"></div>
    </div>
    {% else %}
    <header class="p-4 flex justify-between items-center bg-white border-b">
        <span class="text-xl font-bold">Smile AI</span>
        <a href="https://smilefinancial.in" target="_blank" class="text-blue-600 border border-blue-600 px-3 py-1 rounded-full text-sm">Visit Site</a>
    </header>
    <main id="chat" class="flex-1 overflow-y-auto p-4 flex flex-col"></main>
    <div class="p-4 bg-white border-t">
        <div class="gemini-input-bar">
            <i class="fa-solid fa-plus text-gray-500"></i>
            <input type="text" id="userInput" class="flex-1 bg-transparent outline-none" placeholder="Smile AI से पूछें...">
            <i class="fa-solid fa-microphone text-gray-500"></i>
            <button onclick="send()" class="text-blue-600 font-bold ml-2">Send</button>
        </div>
    </div>
    {% endif %}
    <script>
        function onSignIn(r) {
            fetch('/login-sync', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({token:r.credential})})
            .then(() => window.location.reload());
        }
        async function send() {
            const i = document.getElementById('userInput');
            const chat = document.getElementById('chat');
            const val = i.value; if(!val) return;
            chat.innerHTML += `<div class="user-msg">${val}</div>`;
            i.value = "";
            const res = await fetch('/ask-ai', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({query:val})});
            const data = await res.json();
            chat.innerHTML += `<div class="p-2 text-gray-800"><b>S:</b> ${data.reply}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, logged_in=session.get('logged_in'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
