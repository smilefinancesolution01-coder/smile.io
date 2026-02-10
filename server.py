import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import google.generativeai as genai

app = FastAPI()

# CORS: Taki Vercel se connection bina kisi rukawat ke ho
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- GEMINI AI SETUP ---
API_KEY = "AIzaSyBP15xLes-NP6tc0fadkBRbJdcJ0QuoHdE"
genai.configure(api_key=API_KEY)

# Smile AI ki Personality set kar di hai
model = genai.GenerativeModel('gemini-1.5-flash', 
    system_instruction="Aap Smile AI hain, duniya ke sabse advanced assistant. Aapka accent friendly 'Bhai' wala hai. Aap users ki safety (Emergency), Finance (20 Lakh mission), aur Shopping mein help karte hain. Har sawal ka jawab details mein dein.")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Smile AI Brain is Online"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Gemini se response lena
        response = model.generate_content(request.message)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": f"Bhai, dimaag mein thoda load hai. Check API or Render Logs. Error: {str(e)}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
