import os
import json
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

app = Flask(__name__)
CORS(app)

# Render se JSON credentials uthana
if os.getenv("GOOGLE_CREDS"):
    creds_dict = json.loads(os.getenv("GOOGLE_CREDS"))
    credentials = service_account.Credentials.from_service_account_info(creds_dict)
    
    # Vertex AI Initialize
    vertexai.init(
        project="smile-ai-486910", 
        location="us-central1", 
        credentials=credentials
    )
    model = GenerativeModel("gemini-1.5-flash")

@app.route('/')
def home():
    return "Smile AI: Vertex AI (LEGENDARY MODE) is LIVE!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Vertex Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
