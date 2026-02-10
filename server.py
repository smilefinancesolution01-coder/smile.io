import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# API Setup
os.environ["GOOGLE_API_KEY"] = "AIzaSyBP15xLes-NP6tc0fadkBRbJdcJ0QuoHdE"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# AI ko instructions dena (Amazon links aur shopping ke liye)
system_instruction = (
    "Aap Smile AI ho, ek expert financial aur shopping assistant. "
    "Agar user kisi product ke baare mein puche, toh Amazon.in ke links suggest karein. "
    "Financial queries ka sahi jawab dein aur keywords ka use karein."
)

# FIXED MODEL NAME: 404 error hatane ke liye
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_instruction
)

@app.route('/')
def home():
    return "Smile AI Server is Running!"

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
        # Agar phir bhi model fail ho, toh backup model use karega
        return jsonify({"reply": "Bhai, AI thoda busy hai. Ek baar refresh karke puchiye."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
