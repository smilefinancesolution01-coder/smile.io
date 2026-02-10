import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# AAPKI KEY
API_KEY = "AIzaSyCJCmyILSlIl4gYA8-7cFcTtlL3_KvYYR4"

# MODEL CHANGE: gemini-1.5-flash ki jagah gemini-pro use kar rahe hain
# Ye har key par chalta hai bina 404 ke
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

@app.route('/')
def home():
    return "Smile AI: RAMBAN v2 is LIVE!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_data = request.json
        user_text = user_data.get("message", "")

        payload = {
            "contents": [{
                "parts": [{"text": user_text}]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(GEMINI_URL, json=payload, headers=headers)
        result = response.json()

        if "candidates" in result:
            ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": ai_reply})
        else:
            # Agar abhi bhi error aaye toh poora detail dikhao
            return jsonify({"reply": f"Google Response: {str(result)}"}), 500

    except Exception as e:
        return jsonify({"reply": f"System Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
