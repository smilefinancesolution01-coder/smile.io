import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Render ke Environment Variable se credentials lena
def get_access_token():
    creds = json.loads(os.getenv("GOOGLE_CREDS"))
    # Token nikalne ka simple logic (Standard API call ke liye)
    return os.getenv("API_KEY") # Agar aapke paas API key hai toh wo best hai

@app.route('/')
def home():
    return "Smile AI: Server is Fixed and Running!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # HUM WAPAS DIRECT API PAR AA RAHE HAIN PAR NAYE MODEL KE SAATH
        # Kyunki Vertex AI setup Render par 'Status 1' de raha hai
        API_KEY = "AIzaSyAZ0Wb-DfNIdDMitOWxrvtDjuKTgzwGca8"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        payload = {
            "contents": [{"parts": [{"text": user_msg}]}]
        }
        
        response = requests.post(url, json=payload)
        result = response.json()
        
        if "candidates" in result:
            return jsonify({"reply": result['candidates'][0]['content']['parts'][0]['text']})
        else:
            return jsonify({"reply": "Google Error: " + str(result)}), 500
            
    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
