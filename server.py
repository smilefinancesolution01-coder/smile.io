import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Render ki settings se API key uthayega
API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# Gemini 1.5 Flash Model (Latest & Stable)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"reply": "Bhai, kuch likhoge tabhi toh bataunga!"}), 400

        # AI Response generate karna
        response = model.generate_content(user_message)
        
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Backend Error: Model connect nahi ho raha. Logs check karein."}), 500

if __name__ == "__main__":
    # Render ke liye port 10000 zaroori hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
