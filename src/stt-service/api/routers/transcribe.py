import logging
from fastapi import APIRouter, UploadFile, File
from typing import Dict, Any

import torch
##from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC


from core.pipelines.pipeline import Pipeline
from core.filters.trim_leading_silence import TrimLeadingSilence
from core.filters.amplify import Amplify
from core.filters.trim_trailing_silence import TrimTrailingSilence
from core.filters.resample import ResampleTo16k
from core.filters.band_pass_filter import BandPassFilter 
from api.resources.transcribe_response import FilteredTranscriptionResponse
from api.resources.transcribe_response import TranscriptionResponse
from core.models.facebook_wav2vec import FacebookWav2vec2LargeXslr53Italian

logger = logging.getLogger("stt-service")

class TranscribeRouter:
    def __init__(self):
        self.router = APIRouter()
        self.pipeline = Pipeline([
            ResampleTo16k(),
            Amplify(),
            BandPassFilter(),
            TrimLeadingSilence(),
            TrimTrailingSilence(),
        ])

        self.pipeline1 = Pipeline([
            ResampleTo16k(),
        ])

        self.model = FacebookWav2vec2LargeXslr53Italian()


        self.router.post("/filter-transcribe", response_model=FilteredTranscriptionResponse)(self.transcribe)
        self.router.post("/transcribe", response_model=TranscriptionResponse)(self.filterAndTranscribe)

    async def transcribe(self, file: UploadFile = File(...)) -> FilteredTranscriptionResponse:
        logger.info("Transcription started...")
        audio_bytes = await file.read()

        logger.info("Running model inference...")
        transcription, confidence = self.model.process(audio_bytes)

        logger.info(f"Transcription result: {transcription}") 

        return FilteredTranscriptionResponse(
            transcription=transcription,
            confidence=0.9,
        )


    async def filterAndTranscribe(self, file: UploadFile = File(...)) -> FilteredTranscriptionResponse:
        logger.info("Filtered-Transcription started...")
        audio_bytes = await file.read()

        filter_outcomes, waveform = self.pipeline.run(audio_bytes)

        logger.info("Running model inference...")
        transcription, confidence = self.model.process(waveform)

        logger.info(f"Transcription result: {transcription}") 

        return FilteredTranscriptionResponse(
            input_file=filter_outcomes[0]["input_file"],
            transformations=filter_outcomes,
            transcription=transcription,
            output_file=filter_outcomes[-1]["output_file"],
            confidence=0.9,
        )

# Expose router instance
router = TranscribeRouter().router
