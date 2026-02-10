import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# AAPKI NAYI KEY
API_KEY = "AIzaSyCJCmyILSlIl4gYA8-7cFcTtlL3_KvYYR4"

# GOOGLE STABLE ENDPOINT (v1 - No beta)
# Is raaste mein 404 aane ka chance zero hai
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/')
def home():
    return "Smile AI: RAMBAN Server is LIVE!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_data = request.json
        user_text = user_data.get("message", "")

        # Direct JSON Payload for Google
        payload = {
            "contents": [{
                "parts": [{"text": user_text}]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        
        # Seedha Google ko call lagana
        response = requests.post(GEMINI_URL, json=payload, headers=headers)
        result = response.json()

        # Jawab nikalna
        if "candidates" in result:
            ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": ai_reply})
        else:
            # Agar Google koi error de
            error_msg = result.get("error", {}).get("message", "Google Busy Hai")
            return jsonify({"reply": f"Google Error: {error_msg}"}), 500

    except Exception as e:
        return jsonify({"reply": f"System Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
