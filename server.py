import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from google.generativeai import client

app = Flask(__name__)
CORS(app)

# API KEY Setup
API_KEY = "AIzaSyCJCmyILSlIl4gYA8-7cFcTtlL3_KvYYR4"

# VERSION LOCK: Forcefully using v1 instead of v1beta
genai.configure(api_key=API_KEY, transport='rest')

# Using 'gemini-1.5-flash' without '-latest' or prefixes
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "Smile AI: Server is Fixed and Stable!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # Simple content generation
        response = model.generate_content(user_msg)
        
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {str(e)}")
        # Agar phir bhi 404 aaye, toh hum 'gemini-pro' par switch karenge automatic
        try:
            backup_model = genai.GenerativeModel('gemini-pro')
            response = backup_model.generate_content(user_msg)
            return jsonify({"reply": response.text})
        except:
            return jsonify({"reply": "Bhai, API Key refresh hone mein time le rahi hai. 2 min ruko."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
