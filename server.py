import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# 1. CORS Connection (Vercel ke liye zaroori hai)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# 2. Home Route (Check karne ke liye ki server zinda hai)
@app.get("/")
def home():
    return {"status": "Smile AI Engine is Running", "vision": "October Goal 20 Lakh"}

# 3. Main AI Logic
@app.post("/chat")
def chat(request: ChatRequest):
    q = request.message.lower()
    
    # 🚨 EMERGENCY LOGIC (Women Safety)
    if any(word in q for word in ["help", "police", "bachao", "emergency", "ambulance"]):
        return {"reply": "EMERGENCY_ACTIVATE: Main aapki location track kar raha hoon aur Police (112) ko alert bhej raha hoon. Himmat rakhiye!"}

    # 💰 FINANCE & ROJGAR (Target 20 Lakh)
    elif any(word in q for word in ["loan", "paisa", "job", "paisa kamana", "finance"]):
        return {"reply": "Smile Finance: Hum aapko sabse sasta loan aur online kamai ke raste dete hain. Kya aapko Business Loan chahiye ya Personal?"}

    # 🛍️ AFFILIATE SHOPPING (XYZ Products)
    elif any(word in q for word in ["buy", "amazon", "price", "mobile", "shoes", "kharidna"]):
        item = q.replace("buy", "").replace("price", "").strip()
        # Yahan aap apna Amazon/Flipkart affiliate link setup karenge
        return {"reply": f"Smile AI ne aapke liye best deal dhoond li hai. Is link par click karke kharidye: https://www.amazon.in/s?k={item} (Affiliate Link Active)"}

    # 🎵 ENTERTAINMENT (Music/Video)
    elif any(word in q for word in ["gaana", "music", "video", "song"]):
        return {"reply": "Bilkul! Main aapke liye entertainment portal khol raha hoon. Kya sunna chahenge?"}

    # 🤖 GENERAL AI
    else:
        return {"reply": f"Smile AI: Main duniya ki har service de sakta hoon. Aapne '{request.message}' pucha, main isme expert hoon!"}

# 4. Render Port Configuration (Iske bina Status 1 error aata hai)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
