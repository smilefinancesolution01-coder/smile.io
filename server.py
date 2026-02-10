import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# AAPKI NAYI API KEY (Isse maine fix kar diya hai)
API_KEY = "AIzaSyAZ0Wb-DfNIdDMitOWxrvtDjuKTgzwGca8"

# GOOGLE STABLE V1 ENDPOINT (Ramban Formula)
# Is URL se 404 error hamesha ke liye khatam ho jayega
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/')
def home():
    return "Smile AI: RAMBAN v3 (ULTRA STABLE) is LIVE!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_data = request.json
        user_text = user_data.get("message", "")

        # Google Gemini v1 format
        payload = {
            "contents": [{
                "parts": [{"text": user_text}]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        
        # Direct API Call for Super Fast Speed
        response = requests.post(GEMINI_URL, json=payload, headers=headers)
        result = response.json()

        # Extracting Reply
        if "candidates" in result:
            ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": ai_reply})
        else:
            # Detailed Error Reporting if Google gives any issue
            error_msg = result.get("error", {}).get("message", "API Key active hone mein time le rahi hai.")
            return jsonify({"reply": f"Google Update: {error_msg}"}), 500

    except Exception as e:
        return jsonify({"reply": f"System Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
