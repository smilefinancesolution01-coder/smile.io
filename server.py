import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS fix for Vercel connection
CORS(app, resources={r"/*": {"origins": "*"}})

# AAPKI NAYI KEY
API_KEY = "AIzaSyAZ0Wb-DfNIdDMitOWxrvtDjuKTgzwGca8"

# Is baar hum v1beta ke saath gemini-1.0-pro use kar rahe hain
# Ye combo un keys ke liye hai jo 1.5 flash nahi dhoond pa rahi
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent?key={API_KEY}"

@app.route('/')
def home():
    return "Smile AI: RAMBAN v4 (Legacy Stable) is LIVE!"

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

        # Success check
        if "candidates" in result:
            ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": ai_reply})
        else:
            # Full Debugging: Agar ab bhi error aaye toh poora message dikhega
            return jsonify({"reply": f"Google Response: {str(result)}"}), 500

    except Exception as e:
        return jsonify({"reply": f"System Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
