import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# NAYI API KEY JO AAPNE ABHI DI HAI
API_KEY = "AIzaSyAZ0Wb-DfNIdDMitOWxrvtDjuKTgzwGca8"

# STABLE ENDPOINT: v1 (No beta) aur model ka sahi naam
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/')
def home():
    return "Smile AI: RAMBAN v3 (Stable) is LIVE!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_data = request.json
        user_text = user_data.get("message", "")

        # Correct JSON format for Gemini v1
        payload = {
            "contents": [{
                "parts": [{"text": user_text}]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(GEMINI_URL, json=payload, headers=headers)
        result = response.json()

        # Reply extraction
        if "candidates" in result:
            ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": ai_reply})
        else:
            # Full error tracking agar ab bhi fail ho
            return jsonify({"reply": f"Google Update: {str(result)}"}), 500

    except Exception as e:
        return jsonify({"reply": f"System Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
