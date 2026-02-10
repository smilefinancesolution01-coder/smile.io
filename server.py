import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Nayi API Key
genai.configure(api_key="AIzaSyCJCmyILSlIl4gYA8-7cFcTtlL3_KvYYR4")

@app.route('/')
def home(): return "Smile AI: Online"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # Sabse purana aur stable model use kar rahe hain jo 404 nahi deta
        model = genai.GenerativeModel('gemini-pro') 
        
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})
        
    except Exception as e:
        # Agar gemini-pro bhi fail ho, toh flash try karein
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(user_msg)
            return jsonify({"reply": response.text})
        except Exception as e2:
            return jsonify({"reply": f"Google Error: {str(e2)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
