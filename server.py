import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# API KEY Setup
API_KEY = "AIzaSyBP15xLes-NP6tc0fadkBRbJdcJ0QuoHdE"
genai.configure(api_key=API_KEY)

# STABLE MODEL: Gemini-pro sabse zada compatible hai
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
    return "Smile AI is LIVE and Ready!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # Simple generation call
        response = model.generate_content(user_msg)
        
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "AI ne koi jawab nahi diya, phir se puchein."})
            
    except Exception as e:
        print(f"Error: {str(e)}")
        # Backup message agar phir bhi error aaye
        return jsonify({"reply": "Bhai, API key ya model mein issue hai. Please check Google AI Studio."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
