from pydantic import BaseModel
from typing import Optional, List


class SourceAudioResponse(BaseModel):
    source_name: str
    speaker: Optional[str] = None
    audio_url: str

class PhraseResponse(BaseModel):
    id: str
    text: str
    translation: str
    level: str
    categories: List[str]
    sources: List[SourceAudioResponse]
