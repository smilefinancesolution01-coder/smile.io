import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS ko pura open rakha hai taaki Vercel se connection fail na ho
CORS(app, resources={r"/*": {"origins": "*"}})

# AAPKI EKDOM NAYI API KEY
API_KEY = "AIzaSyAdOj2bPfxGfKDDcrNyjGVZ7QMVpYj0XLI"

# Gemini 1.5 Flash ka Direct Endpoint
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/')
def home():
    return "Smile AI: NEW KEY ENGINE IS LIVE!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_data = request.json
        user_text = user_data.get("message", "")

        if not user_text:
            return jsonify({"reply": "Bhai, kuch message toh likho!"}), 400

        # Google Gemini Format
        payload = {
            "contents": [{
                "parts": [{"text": user_text}]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(GEMINI_URL, json=payload, headers=headers)
        result = response.json()

        # Reply nikalne ki koshish
        if "candidates" in result:
            ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": ai_reply})
        else:
            # Agar koi error aaye toh detail dikhayega
            error_msg = result.get("error", {}).get("message", "Unknown Google Error")
            return jsonify({"reply": f"Google Error: {error_msg}"}), 500

    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
