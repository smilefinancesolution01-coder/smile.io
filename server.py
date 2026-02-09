import os
from fastapi import FastAPI
import uvicorn

# Simple FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Smile Finance AI is Running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    # Render se port uthane ke liye
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
