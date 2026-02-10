import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# AAPKI NAYI API KEY
API_KEY = "AIzaSyAdOj2bPfxGfKDDcrNyjGVZ7QMVpYj0XLI"

@app.route('/')
def home():
    return "Smile AI: Server is Live, checking Google connection..."

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        user_data = request.json
        user_text = user_data.get("message", "")
        
        # Hum 2 alag-alag URLs try karenge agar ek fail ho jaye
        urls = [
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}",
            f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
        ]
        
        last_error = ""
        for url in urls:
            payload = {"contents": [{"parts": [{"text": user_text}]}]}
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            
            if "candidates" in result:
                return jsonify({"reply": result['candidates'][0]['content']['parts'][0]['text']})
            else:
                last_error = str(result)

        # Agar dono fail ho jayein toh error dikhao
        return jsonify({"reply": f"Google Error: {last_error}"}), 500

    except Exception as e:
        return jsonify({"reply": f"Internal Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
