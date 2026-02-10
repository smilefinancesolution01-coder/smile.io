import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# CORS for Vercel connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Smile AI Engine is Running"}

@app.post("/chat")
def chat(request: ChatRequest):
    msg = request.message.lower()
    if "help" in msg or "emergency" in msg:
        reply = "EMERGENCY: SOS Activated. Tracking location..."
    elif "loan" in msg:
        reply = "Smile Finance: Aapka loan process ho raha hai."
    else:
        reply = f"Smile AI: Aapne kaha '{request.message}'. Main aapki kaise madad karun?"
    return {"reply": reply}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
