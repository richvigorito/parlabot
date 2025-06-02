from fastapi import APIRouter
from fastapi.responses import JSONResponse
from db.mongo import collection
from api.resources.phrase_response import PhraseResponse
import random

router = APIRouter(prefix="/phrases", tags=["Phrases"])

@router.get("/random", response_model=PhraseResponse)
async def get_random_phrase():
    count = await collection.count_documents({})
    if count == 0:
        return JSONResponse(content={"error": "No phrases found"}, status_code=404)

    skip = random.randint(0, count - 1)
    docs = await collection.find().skip(skip).limit(1).to_list(1)
    if not docs:
        return JSONResponse(content={"error": "Phrase not found"}, status_code=404)

    p = docs[0]
    return PhraseResponse(
        id=str(p["_id"]),
        level=p["level"],
        text=p["text"],
        audio_file=p["audiofile"],
        audio_url=f"/audio/{p['audiofile']}"
    )

