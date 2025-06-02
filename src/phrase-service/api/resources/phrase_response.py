from pydantic import BaseModel

class PhraseResponse(BaseModel):
    id: str
    level: str
    text: str
    audio_file: str
    audio_url: str

