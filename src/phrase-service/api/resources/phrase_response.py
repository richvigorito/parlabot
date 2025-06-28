from pydantic import BaseModel
from typing import Optional, List

from storage.storage_factory import make_storage

storage = make_storage()

class SourceAudioResponse(BaseModel):
    source_name: str
    speaker: Optional[str] = None
    filename: str

    @property
    def audio_url(self) -> str:
        return storage.get_url(self.filename)

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["audio_url"] = self.audio_url
        return data

class PhraseResponse(BaseModel):
    id: str
    text: str
    translation: str
    level: str
    categories: List[str]
    sources: List[SourceAudioResponse]

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["sources"] = [s.dict(*args, **kwargs) for s in self.sources]
        return data


