import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# API KEY setup
API_KEY = "AIzaSyBP15xLes-NP6tc0fadkBRbJdcJ0QuoHdE"
genai.configure(api_key=API_KEY)

# Gemini 1.5 Flash - Best for Mobile and Speed
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "Smile AI Server is LIVE!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message")
        if not user_msg:
            return jsonify({"reply": "Kuch likho bhai!"}), 400
            
        # AI content generation
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": f"Model Busy! Ek baar page refresh karein. Details: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
