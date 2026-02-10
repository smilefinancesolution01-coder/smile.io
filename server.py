import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# API KEY Setup
API_KEY = "AIzaSyBP15xLes-NP6tc0fadkBRbJdcJ0QuoHdE"
genai.configure(api_key=API_KEY)

# YAHAN CHANGE HAI: Stable model configuration
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

# Model initialization without 'models/' prefix
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config
)

@app.route('/')
def home():
    return "<h1>Smile AI Server is LIVE!</h1>"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message")
        
        # Seedha content generate karna (v1 version par)
        response = model.generate_content(user_msg)
        
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Detailed Error: {e}")
        return jsonify({"reply": f"Bhai, connectivity issue hai. Details: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
