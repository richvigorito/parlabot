import logging
from asgi_correlation_id import CorrelationIdMiddleware, correlation_id
from fastapi import FastAPI, UploadFile, File
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import torchaudio
import soundfile as sf
import io
import os
from typing import Tuple, List, Dict, Any

from filters.trim_silence import TrimSilence
from filters.resample import ResampleTo16k
from logging_config import setup_logging

SHARED_VOLUME_PATH = "/app/shared/"  # Mounted shared folder (use a conf later)

# Initialize logging
setup_logging()
logger = logging.getLogger("stt-service")


app = FastAPI()
app.add_middleware(CorrelationIdMiddleware)

# Load model + tokenizer once on startup
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-xlsr-53-italian")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53-italian")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)) -> Dict[str, Any]:
    logger.info(f"transcribe begin......")
    audio_bytes = await file.read()

    logger.info(f"run pipeline......")
    filterOutcomes, waveform = run_filter_pipeline(audio_bytes)
    #waveform = resample_to_16k(audio_bytes)

    # speech_array, sampling_rate = sf.read(io.BytesIO(audio_bytes))
    # input_values = processor(speech_array, sampling_rate=sampling_rate, return_tensors="pt", padding="longest").input_values

    logger.info(f"process waveform against model")
    input_values = processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt", padding="longest").input_values

    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0].lower()
    logger.info(f"Transcription: {transcription}")

    return {
        "input_file": filterOutcomes[0]["input_file"],
        "transformations": filterOutcomes,
        "transcription": transcription,
        "output_file": filterOutcomes[-1]["output_file"],
        "confidence": .9,
    }

def run_filter_pipeline(input_bytes: bytes) -> Tuple[List[Dict[str, Any]], torch.Tensor]:

    pipeline: List[Filter] = [
        ResampleTo16k(),
        TrimSilence(),
    ]

    filterOutcomes = []

    filter_outcomes: List[Dict[str, Any]] = []
    current_bytes = input_bytes

    for idx, f in enumerate(pipeline):
        next_bytes = f.run_filter(current_bytes)
        logger.info(f"[{f.name}] output size: {len(next_bytes)} bytes")


        # Simulate file paths (placeholder logic)
        ### need to write these somewhere on volume or whereever
        ### both stt-service and orchestrator can read from 
        ### somehow ... like orchestrator has an enpoint to grab 
        ### files that the stt writes. ideally the stt doesnt 
        ### have to also have a file endpoint

        input_path = get_write_path(f"step{idx}_{f.name}_input.wav")
        output_path = get_write_path(f"step{idx}_{f.name}_output.wav")


        logger.info(f"input file: {input_path}")
        logger.info(f"output file: {output_path}")

        ## this is inefficient cause writes twice but right now who cares
        write_audio_file(input_path, current_bytes)
        write_audio_file(output_path, next_bytes)

        filter_outcomes.append({
            "filter_name": f.name,
            "input_file": input_path.replace("/app/shared", "/files", 1),
            "output_file": output_path.replace("/app/shared", "/files", 1),
            "metadata": {},
        })

        current_bytes = next_bytes
    waveform, _ = torchaudio.load(io.BytesIO(current_bytes))

    return filter_outcomes, waveform

def write_audio_file(path: str, data: bytes):
   with open(path, "wb") as f:
        f.write(data)

def get_write_path(path: str) -> str:
    path = (correlation_id.get() or "") + "_" + path
    full_path = os.path.join(SHARED_VOLUME_PATH, path)
    logger.info(f"fullpath: {full_path}")
    return full_path




