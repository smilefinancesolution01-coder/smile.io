import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

app = Flask(__name__)

# IS LINE KO DHAYAN SE DEKHO - Ye Vercel ko allow karega
CORS(app, resources={r"/*": {"origins": "*"}})

# Credentials Setup from Environment Variable
creds_json = os.getenv("GOOGLE_CREDS")
model = None

if creds_json:
    try:
        creds_dict = json.loads(creds_json)
        credentials = service_account.Credentials.from_service_account_info(creds_dict)
        vertexai.init(project="smile-ai-486910", location="us-central1", credentials=credentials)
        model = GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        print(f"Vertex Init Error: {e}")

@app.route('/')
def home():
    return "Smile AI: Vertex AI Mode Active & CORS Open!"

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    # CORS pre-flight handling
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        if not model:
            return jsonify({"reply": "System Error: Model not initialized. Check Render Env Variables."}), 500
            
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Vertex Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
