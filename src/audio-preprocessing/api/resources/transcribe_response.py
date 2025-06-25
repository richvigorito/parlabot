from pydantic import BaseModel
from typing import List, Dict

class FilterOutcome(BaseModel):
    filter_name: str
    input_file: str
    output_file: str
    metadata: Dict[str, str]

class TranscribeResponse(BaseModel):
    input_file: str
    transformations: List[FilterOutcome]
    transcription: str
    output_file: str
    confidence: float

