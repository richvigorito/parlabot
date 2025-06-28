import logging
from bson import ObjectId
from db.mongo import collection
from services.tts.provider_factory import get_tts_provider
from config import settings
from uuid import uuid4
from pathlib import Path
from fastapi import UploadFile, HTTPException
from api.resources.phrase_response import PhraseResponse
from api.requests.phrase_request import PhraseInput, PhraseSourceEntry
from typing import Dict, List, Optional

AUDIO_DIR = settings.AUDIO_DIR
SPEAKER = settings.SPEAKER
Path(AUDIO_DIR).mkdir(exist_ok=True)

logger = logging.getLogger("phrase-service")

class NotFoundError(Exception):
    pass

async def create_phrase_with_selected_tts(
    phrase_input: PhraseInput, provider_map: Dict[str, List[str]]) -> PhraseResponse:

    logger.info("Create Select Phrase Service...")
    audio_sources = []

    for provider_name, speakers in provider_map.items():
        provider = get_tts_provider(provider_name)
        logger.info('...provider:' + provider_name)
        for speaker in speakers:
            filename = await generate_tts_audio(phrase_input.text, provider, speaker)
            audio_sources.append({
                "source_name": provider_name,
                "speaker": speaker,
                "filename": filename
            })

    return await save_phrase_doc(phrase_input, audio_sources)

async def create_phrase(phrase_input: PhraseInput) -> PhraseResponse:
    logger.info("Create Phrase Service...")
    filename = f"{uuid4().hex}.wav"
    filepath = Path(AUDIO_DIR) / filename
    tts = get_tts()

    tts.tts_to_file(
        text=phrase_input.text,
        file_path=str(filepath),
        speaker_wav=SPEAKER,
        language="it"
    )

    doc = {
        "text": phrase_input.text,
        "translation": phrase_input.translation,
        "level": phrase_input.level,
        "categories": phrase_input.categories or [],
        "sources": [{
            "source_name": phrase_input.first_source_name,
            "speaker": phrase_input.first_speaker,
            "filename": filename
        }]
    }

    result = await collection.insert_one(doc)

    return PhraseResponse(
        id=str(result.inserted_id),
        text=doc["text"],
        translation=doc["translation"],
        level=doc["level"],
        categories=doc["categories"],
        sources=doc["sources"]
    )

async def add_source_to_phrase(phrase_id: str, source_input: PhraseSourceEntry) -> PhraseResponse:
    oid = ObjectId(phrase_id)
    await collection.update_one(
        {"_id": oid},
        {"$push": {"sources": source_input.dict()}}
    )

    doc = await collection.find_one({"_id": oid})

    return PhraseResponse(
        id=str(doc["_id"]),
        text=doc["text"],
        translation=doc["translation"],
        level=doc["level"],
        categories=doc.get("categories", []),
        sources=doc["sources"]
    )

async def upload_audio_to_source(phrase_id: str, source_name: str, speaker: Optional[str], file: UploadFile) -> str:
    oid = ObjectId(phrase_id)
    doc = await collection.find_one({"_id": oid})
    if not doc:
        raise NotFoundError("Phrase not found")

    sources = doc.get("sources", [])
    source_found = False

    for src in sources:
        if src["source_name"] == source_name and (speaker is None or src.get("speaker") == speaker):
            source_found = True
            ext = Path(file.filename).suffix or ".wav"
            filename = f"{phrase_id}_{source_name}"
            if speaker:
                filename += f"_{speaker}"
            filename += ext
            filepath = Path(AUDIO_DIR) / filename

            contents = await file.read()
            with open(filepath, "wb") as f:
                f.write(contents)

            src["filename"] = filename
            break

    if not source_found:
        raise NotFoundError("Source not found")

    await collection.update_one({"_id": oid}, {"$set": {"sources": sources}})

    return src["filename"]

async def get_phrases(query: dict, offset: int, limit: int):
    docs = await (
        collection.find(query)
        .skip(offset)
        .limit(limit)
        .to_list(limit)
    )

    return [
        PhraseResponse(
            id=str(p["_id"]),
            text=p["text"],
            translation=p["translation"],
            level=p["level"],
            categories=p.get("categories", []),
            sources=p.get("sources", [])
        )
        for p in docs
    ]

async def get_random_phrase(query: dict):
    count = await collection.count_documents(query)
    if count == 0:
        return None

    import random
    skip = random.randint(0, count - 1)
    docs = await collection.find(query).skip(skip).limit(1).to_list(1)

    if not docs:
        return None

    p = docs[0]
    return PhraseResponse(
        id=str(p["_id"]),
        text=p["text"],
        translation=p["translation"],
        level=p["level"],
        categories=p.get("categories", []),
        sources=p.get("sources", [])
    )

async def delete_phrase(phrase_id: str) -> bool:
    oid = ObjectId(phrase_id)
    result = await collection.delete_one({"_id": oid})
    return result.deleted_count > 0

async def generate_tts_audio(text: str, provider, speaker: str) -> str:
    from uuid import uuid4
    filename = f"{uuid4().hex}.wav"
    filepath = Path(AUDIO_DIR) / filename
    #provider.tts_to_file(text=text, file_path=str(filepath), speaker=speaker, language="it")
    provider.synthesize(text=text, speaker=speaker, output_path=str(filepath))
    return filename

async def save_phrase_doc(phrase_input: PhraseInput, sources: List[dict]) -> PhraseResponse:
    doc = {
        "text": phrase_input.text,
        "translation": phrase_input.translation,
        "level": phrase_input.level,
        "categories": phrase_input.categories or [],
        "sources": sources,
    }
    result = await collection.insert_one(doc)
    return PhraseResponse(
        id=str(result.inserted_id),
        text=doc["text"],
        translation=doc["translation"],
        level=doc["level"],
        categories=doc["categories"],
        sources=doc["sources"],
    )
