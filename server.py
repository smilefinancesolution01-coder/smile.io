import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# NAYI KEY YAHAN HAI
genai.configure(api_key="AIzaSyCJCmyILSlIl4gYA8-7cFcTtlL3_KvYYR4")

# Personal Financial Assistant Instructions
instructions = (
    "Aap Smile AI ho, ek professional financial assistant. "
    "1. Keywords use karo. 2. Shopping ke liye Amazon.in links do. "
    "3. Hamesha helpful aur mobile-friendly response do."
)

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=instructions
)

@app.route('/')
def home():
    return "Smile AI is LIVE with New Key!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        if not user_msg:
            return jsonify({"reply": "Kuch toh likho!"}), 400
            
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": f"Key Active ho rahi hai, 1 min ruko. Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
