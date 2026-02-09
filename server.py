import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# IMPORTANT: Ye Vercel aur Render ko aapas mein jodta hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Isse aapki Vercel site connect ho payegi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Smile Finance AI Engine is Running!"}

@app.post("/chat")
def chat(request: ChatRequest):
    user_query = request.message.lower()
    
    # PREMIUM SALES LOGIC (Month 1: Lead Generation)
    if "loan" in user_query or "paisa" in user_query:
        reply = "Smile Finance mein aapka swagat hai! Hum aapko market se kam interest par loan dila sakte hain. Kya aap apni monthly income aur phone number share karenge taaki hamare advisor aapko call kar sakein?"
    
    elif "credit card" in user_query:
        reply = "Aapke liye hamare paas 3 best Credit Cards hain jo 100% approval dete hain. Kya main unka link yahan share karu?"
    
    else:
        # Default AI Response
        reply = f"Aapka swagat hai Smile Finance AI mein. Aapne kaha: '{request.message}'. Main aapki financial growth mein kaise madad kar sakta hoon?"

    return {"reply": reply}

if __name__ == "__main__":
    # Render ke liye zaroori port setting
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
