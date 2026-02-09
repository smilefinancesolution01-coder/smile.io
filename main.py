import requests
from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# TEST HTML - Isse white screen nahi aayegi
HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>Smile AI Live</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0a0e14; color: white; font-family: sans-serif; text-align: center; padding-top: 50px; }
        .container { border: 2px solid #00f2fe; display: inline-block; padding: 40px; border-radius: 20px; box-shadow: 0 0 20px #00f2fe; }
        h1 { color: #00f2fe; margin-bottom: 10px; }
        .status { color: #2ecc71; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>SMILE FINANCIAL AI</h1>
        <p class="status">● SYSTEM ONLINE & LIVE</p>
        <p>Aapka AI Advisor taiyaar hai.</p>
        <br>
        <a href="tel:7290977231" style="background:#2ecc71; color:white; padding:10px 20px; text-decoration:none; border-radius:10px;">Call Support</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000)) # Render ke liye port fix
    app.run(host='0.0.0.0', port=port)
