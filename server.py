import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# API Key fix
API_KEY = "AIzaSyCJCmyILSlIl4gYA8-7cFcTtlL3_KvYYR4"

# Forcefully configure using the most stable method
try:
    genai.configure(api_key=API_KEY)
    # Yahan hum model ko bina version prefix ke call karenge
    model = genai.GenerativeModel('gemini-pro') 
    # 'gemini-pro' har API key par 100% chalta hai 404 nahi deta
except Exception as e:
    print(f"Setup Error: {e}")

@app.route('/')
def home():
    return "Smile AI Server is LIVE and STABLE!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # Simple response generation
        response = model.generate_content(user_msg)
        
        if response and response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "AI ne jawab nahi diya, phir se puchein."})
            
    except Exception as e:
        error_str = str(e)
        print(f"Chat Error: {error_str}")
        # Agar abhi bhi v1beta bole, toh hum error message badal denge
        return jsonify({"reply": f"Bhai, API mein issue hai: {error_str}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
