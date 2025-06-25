import logging
from fastapi import APIRouter, Query, File, Path, Body, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from api.resources.phrase_response import PhraseResponse
from api.requests.phrase_request import PhraseInput, PhraseSourceEntry
from api.routers.dependencies import get_pagination_params, PaginationParams
import services.phrase_service as phrase_service
from services.tts.provider_factory import build_provider_map, build_provider_map_from_path

router = APIRouter(tags=["Phrases"])
logger = logging.getLogger("phrase-service")

def get_phrase_filters(
    level: str = Query(None),
    text: str = Query(None),
) -> dict:
    filters = {}
    if level:
        filters["level"] = level
    if text:
        filters["text"] = {"$regex": text, "$options": "i"}
    return filters

@router.post("/phrases", response_model=PhraseResponse)
async def create_phrase_with_all_tts(phrase_input: PhraseInput = Body(...)):
    provider_map = build_provider_map()
    return await phrase_service.create_phrase_with_selected_tts(phrase_input, provider_map)


@router.post("/tts/{providers_speakers}/phrases", response_model=PhraseResponse)
async def create_phrase_with_selected_tts(
    phrase_input: PhraseInput = Body(...),
    providers_speakers: str = Path(...)
):
    provider_map = build_provider_map_from_path(providers_speakers)
    return await phrase_service.create_phrase_with_selected_tts(phrase_input, provider_map)

@router.patch("/phrases/{phrase_id}/sources", response_model=PhraseResponse)
async def add_source_to_phrase(phrase_id: str, source_input: PhraseSourceEntry):
    phrase = await phrase_service.add_source_to_phrase(phrase_id, source_input)
    return phrase

@router.patch("/phrases/{phrase_id}/sources/{source_name}/audio")
async def upload_audio_for_source(
    phrase_id: str,
    source_name: str,
    speaker: Optional[str] = Query(None),
    file: UploadFile = File(...)
):
    try:
        audio_url = await phrase_service.upload_audio_to_source(phrase_id, source_name, speaker, file)
    except phrase_service.NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"audio_url": audio_url}

@router.get("/phrases", response_model=List[PhraseResponse])
async def get_phrases(
    query: dict = Depends(get_phrase_filters),
    pagination: PaginationParams = Depends(get_pagination_params)
):
    phrases = await phrase_service.get_phrases(query, pagination.offset, pagination.limit)
    if not phrases:
        return JSONResponse(content={"error": "no phrases found"}, status_code=404)
    return phrases

@router.get("/phrases/random", response_model=PhraseResponse)
async def get_random_phrase(query: dict = Depends(get_phrase_filters)):
    phrase = await phrase_service.get_random_phrase(query)
    if not phrase:
        return JSONResponse(content={"error": "no phrases found"}, status_code=404)
    return phrase

@router.delete("/phrases/{phrase_id}", status_code=204)
async def delete_phrase(phrase_id: str):
    success = await phrase_service.delete_phrase(phrase_id)
    if not success:
        raise HTTPException(status_code=404, detail="Phrase not found")

