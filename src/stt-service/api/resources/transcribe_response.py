from pydantic import BaseModel
from typing import List, Dict

class FilterOutcome(BaseModel):
    filter_name: str
    input_file: str
    output_file: str
    metadata: Dict[str, str]

class FilteredTranscriptionResponse(BaseModel):
    input_file: str
    transformations: List[FilterOutcome]
    output_file: str
    transcription: str
    confidence: float
#    transcriptionV2: TranscriptionResponse

class TranscriptionResponse(BaseModel):
    transcription: str
    confidence: float


