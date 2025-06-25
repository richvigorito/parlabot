# api/requests/source_request.py
from pydantic import BaseModel
from typing import Optional

class SourceInput(BaseModel):
    source_name: str
    speaker: str
    language: Optional[str] = "it"
    notes: Optional[str] = None
