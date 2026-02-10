import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# API Key setup
API_KEY = "AIzaSyBP15xLes-NP6tc0fadkBRbJdcJ0QuoHdE"
genai.configure(api_key=API_KEY)

# STABLE MODEL FIX: 404 error hatane ke liye
# Hum yahan 'gemini-1.5-flash' use kar rahe hain jo stable hai
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "<h1>Smile AI Server is LIVE!</h1>"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message")
        
        # Generation config add karne se 404 ke chances kam ho jate hain
        response = model.generate_content(user_msg)
        
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error details: {e}")
        # Agar 404 aata hai toh ye version ka issue hai
        return jsonify({"reply": f"Model connectivity issue! Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
