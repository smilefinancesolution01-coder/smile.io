import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# AAPKI KEY
API_KEY = "AIzaSyCJCmyILSlIl4gYA8-7cFcTtlL3_KvYYR4"

# FINAL UPDATED URL (v1 version + flash model)
# Ye combo sabse zyada stable hai free accounts ke liye
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/')
def home():
    return "Smile AI: FINAL STABLE VERSION IS LIVE!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_data = request.json
        user_text = user_data.get("message", "")

        # Payload Structure for v1
        payload = {
            "contents": [{
                "parts": [{"text": user_text}]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(GEMINI_URL, json=payload, headers=headers)
        result = response.json()

        # Check for success
        if "candidates" in result:
            ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": ai_reply})
        else:
            # Full error reporting for debugging
            return jsonify({"reply": f"Google Update: {result.get('error', {}).get('message', 'Check API Key Permission')}"}), 500

    except Exception as e:
        return jsonify({"reply": f"System Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
