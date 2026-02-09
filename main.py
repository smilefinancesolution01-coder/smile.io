import requests
from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# Aapka Pura GPT-5 wala HTML yahan paste karein
HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>Smile Financial AI</title>
    <style>
        body { background: #05070a; color: white; font-family: sans-serif; text-align: center; padding: 50px; }
        .box { border: 1px solid #00f2fe; padding: 20px; border-radius: 15px; display: inline-block; }
    </style>
</head>
<body>
    <div class="box">
        <h1>SMILE FINANCIAL AI</h1>
        <p>System is Live and Ready.</p>
        <a href="tel:7290977231" style="color: #2ecc71;">Call: 7290977231</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    try:
        # Agar ye fail hoga toh error screen par dikhega, white screen nahi aayegi
        return render_template_string(HTML_CODE)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    # Render ke liye port setting zaroori hai
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
