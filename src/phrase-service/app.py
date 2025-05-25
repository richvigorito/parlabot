from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
import os
import random

app = FastAPI()
#MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")

client = AsyncIOMotorClient(MONGO_URL)
db = client["phrases"]
collection = db["italian"]

audio_dir = os.path.join(os.path.dirname(__file__), "audio")
app.mount("/audio", StaticFiles(directory=audio_dir), name="audio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def health():
    return {"ok"}



@app.get("/phrase/random")
async def get_random_phrase():
    count = await collection.count_documents({})
    if count == 0:
        return JSONResponse(content={"error": "No phrases found"}, status_code=404)

    skip = random.randint(0, count - 1)
    doc = await collection.find().skip(skip).limit(1).to_list(1)

    if not doc:
        return JSONResponse(content={"error": "Phrase not found"}, status_code=404)
   
    p = doc[0]

    return {
        "id": str(p["_id"]),
        "level": p["level"],
        "text": p["text"],
        "audio_file": p["audiofile"],
        "audio_url": f"/audio/{p['audiofile']}"
    }
