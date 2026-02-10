import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# API KEY
API_KEY = "AIzaSyCJCmyILSlIl4gYA8-7cFcTtlL3_KvYYR4"

# Configuration ko v1 (Stable) par force karna
genai.configure(api_key=API_KEY)

# MODEL FIX: 'gemini-1.5-flash-latest' use karein jo har version par supported hai
model = genai.GenerativeModel('gemini-1.5-flash-latest')

@app.route('/')
def home():
    return "Smile AI: System Stable & Live!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # Generation call
        response = model.generate_content(user_msg)
        
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "AI khamosh hai, dobara puchein."})
            
    except Exception as e:
        print(f"Detailed Error: {e}")
        # Agar abhi bhi error aaye toh ye direct dikhayega
        return jsonify({"reply": f"Model Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
