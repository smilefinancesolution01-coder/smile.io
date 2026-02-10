import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# AAPKI EKDOM NAYI API KEY
API_KEY = "AIzaSyAdOj2bPfxGfKDDcrNyjGVZ7QMVpYj0XLI"

@app.route('/')
def home():
    return "Smile AI: Debug Mode Active!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")

        # Payload for Gemini
        payload = {
            "contents": [{"parts": [{"text": user_msg}]}]
        }
        
        # Try Version 1 First
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        response = requests.post(url, json=payload)
        result = response.json()

        # If v1 fails, try v1beta
        if "error" in result:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            response = requests.post(url, json=payload)
            result = response.json()

        if "candidates" in result:
            reply = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": reply})
        else:
            return jsonify({"reply": f"Google Keh Raha Hai: {str(result.get('error', {}).get('message', 'Unknown Error'))}"}), 500

    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
