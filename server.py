import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Apni Google API Key yahan dalo
genai.configure(api_key="YOUR_GOOGLE_API_KEY")

# Model setup - Gemini 1.5 Flash latest version
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message")
        
        # AI se response mangna
        response = model.generate_content(user_msg)
        
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Bhai, backend model connect nahi ho raha. API key check karein."}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
