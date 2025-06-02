import logging
from fastapi import APIRouter, UploadFile, File
from typing import Dict, Any

import torch
##from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC


from core.pipelines.pipeline import Pipeline
from core.filters.trim_silence import TrimSilence
from core.filters.resample import ResampleTo16k
from api.resources.transcribe_response import TranscribeResponse
from core.models.facebook_wav2vec import FacebookWav2vec2LargeXslr53Italian

logger = logging.getLogger("stt-service")

class TranscribeRouter:
    def __init__(self):
        self.router = APIRouter()
        self.pipeline = Pipeline([
            ResampleTo16k(),
            TrimSilence(),
        ])

        self.pipeline1 = Pipeline([
            ResampleTo16k(),
        ])

        self.model = FacebookWav2vec2LargeXslr53Italian()


        self.router.post("/transcribe", response_model=TranscribeResponse)(self.transcribe)

    async def transcribe(self, file: UploadFile = File(...)) -> TranscribeResponse:
        logger.info("Transcription started...")
        audio_bytes = await file.read()

        filter_outcomes, waveform = self.pipeline.run(audio_bytes)

        logger.info("Running model inference...")
        transcription, confidence = self.model.process(waveform)

        logger.info(f"Transcription result: {transcription}") 

        return TranscribeResponse(
            input_file=filter_outcomes[0]["input_file"],
            transformations=filter_outcomes,
            transcription=transcription,
            output_file=filter_outcomes[-1]["output_file"],
            confidence=0.9,
        )

# Expose router instance
router = TranscribeRouter().router
