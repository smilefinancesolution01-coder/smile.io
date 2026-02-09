import os
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import google.generativeai as genai

# 1. FastAPI Setup
app = FastAPI()

# 2. Gemini AI Setup (Yahan apni API Key daalna agar baad mein chahiye ho)
# Abhi ke liye hum ise simple rakh rahe hain taaki server start ho jaye
@app.get("/")
def home():
    return {"message": "Smile Finance AI Server is Live!", "status": "Success"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 3. Main Logic for Port Binding (Ye Render ke liye sabse zaroori hai)
if __name__ == "__main__":
    # Render automatically sets a PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting server on port {port}...")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
