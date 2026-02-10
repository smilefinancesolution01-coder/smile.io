import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Ye guard hai
import google.generativeai as genai

app = Flask(__name__)
CORS(app) # Sabhi requests ko allow karne ke liye

# API Setup
os.environ["GOOGLE_API_KEY"] = "AIzaSyBP15xLes-NP6tc0fadkBRbJdcJ0QuoHdE"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "<h1>Smile AI Server is LIVE!</h1>"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message")
        if not user_msg:
            return jsonify({"reply": "Kuch likho bhai!"}), 400
            
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Model Error: AI thoda thak gaya hai, phir se try karein."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
