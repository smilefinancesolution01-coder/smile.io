import requests
from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# Yahan wahi HTML code aayega jo maine pehle diya tha (Voice aur Green word wala)
HTML_CODE = """
<!DOCTYPE html>
<html>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    q = data.get('query', "").lower()
    img = data.get('image')
    api_key = "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"
    
    needs_call = any(x in q for x in ["free", "service", "website", "loan", "advice", "mufat"])
    model = "llama-3.2-11b-vision-preview" if img else "llama-3.3-70b-versatile"
    
    sys_msg = "You are Smile Financial GPT-5 Advisor. Professional human personality. Plain text only. Call 7290977231."
    msgs = [{"role": "system", "content": sys_msg}]
    
    if img:
        msgs.append({"role": "user", "content": [{"type": "text", "text": q or "Analyze."}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}}]})
    else:
        msgs.append({"role": "user", "content": q})

    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {api_key}"}, json={"model": model, "messages": msgs, "temperature": 0.4})
        reply = r.json()['choices'][0]['message']['content'].replace('*', '').replace('#', '')
    except:
        reply = "Please call 7290977231."
    
    return jsonify({"reply": reply, "call_logic": needs_call})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
