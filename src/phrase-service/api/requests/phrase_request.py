from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId

class PhraseSourceEntry(BaseModel):
    source_id: str  
    audio_url: str  

class PhraseInput(BaseModel):
    text: str
    translation: str
    level: str
    categories: Optional[List[str]] = []
    sources: Optional[List[PhraseSourceEntry]] = []
