import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Nayi API Key
API_KEY = "AIzaSyCJCmyILSlIl4gYA8-7cFcTtlL3_KvYYR4"
genai.configure(api_key=API_KEY)

# STABLE MODEL CHOICE: Gemini-pro 404 error nahi deta
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
    return "Smile AI: Connection Successful!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # Simple content generation
        response = model.generate_content(user_msg)
        
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "AI ne jawab nahi diya, phir se try karein."})
            
    except Exception as e:
        print(f"Error: {str(e)}")
        # Agar phir bhi 404 aaye, toh iska matlab Google backend update ho raha hai
        return jsonify({"reply": "Bhai, Google server thoda slow hai. 1 min ruk kar 'Hi' likho."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
