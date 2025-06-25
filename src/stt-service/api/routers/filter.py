import logging
import io
from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from enum import Enum
from core.filters.trim_leading_silence import TrimLeadingSilence
from core.filters.trim_trailing_silence import TrimTrailingSilence

logger = logging.getLogger("stt-service")

class FilterName(str, Enum):
    TRIM_TRAILING_SILENCE = "trim-trailing-silence"
    TRIM_LEADING_SILENCE = "trim-leading-silence"
    # OTHER = "other"  # add more filters here

class FilterRouter:
    def __init__(self):
        self.router = APIRouter()

        self.FILTERS = {
            FilterName.TRIM_TRAILING_SILENCE: TrimTrailingSilence,
            FilterName.TRIM_LEADING_SILENCE: TrimLeadingSilence,
        }

        self.router.post("/filters/{filter_name}")(self.run_filter)

    async def run_filter(self, filter_name: FilterName, file: UploadFile = File(...)):
        # Validate filter
        if filter_name not in self.FILTERS:
            raise HTTPException(status_code=400, detail=f"Unknown filter: {filter_name}")

        audio_bytes = await file.read()

        filter_class = self.FILTERS[filter_name]()
        filtered_audio = filter_class.run_filter(audio_bytes)

        logger.info(f"Applied filter: {filter_name}")

        return Response(content=filtered_audio, media_type="audio/wav")

router = FilterRouter().router
