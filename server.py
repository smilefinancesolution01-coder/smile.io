import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# CORS ko aise set kiya hai taaki Vercel se koi blockage na ho
CORS(app, resources={r"/*": {"origins": "*"}})

# API Key setup
API_KEY = "AIzaSyBP15xLes-NP6tc0fadkBRbJdcJ0QuoHdE"
genai.configure(api_key=API_KEY)

# Generation settings (isase response fast aur stable aata hai)
generation_config = {
  "temperature": 0.9,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Model Setup - 1.5-flash sabse advance hai
# Humne yahan model name check kar liya hai jo stable v1 version par hai
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

@app.route('/')
def home():
    return "<h1>Smile AI Server is LIVE!</h1><p>Status: Working Smoothly</p>"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message")
        
        if not user_msg:
            return jsonify({"reply": "Bhai, message khali hai!"}), 400

        # AI se response mangna
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_msg)
        
        return jsonify({"reply": response.text})
    
    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}")
        # Specific Error Messages
        if "404" in str(e):
            return jsonify({"reply": "Model Error 404: Please check library version in requirements.txt"}), 404
        return jsonify({"reply": f"Server Side Error: {str(e)}"}), 500

if __name__ == "__main__":
    # Render ke liye port management
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
