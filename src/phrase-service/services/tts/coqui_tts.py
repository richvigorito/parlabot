# /app/services/tts/coqui_tts.py
import os
from TTS.api import TTS
from services.tts.base import TTSProvider
from typing import List

os.environ["COQUI_TOS_AGREED"] = "1"

COQUI_SPEAKERS = {
    "common_voice_it_42329444": "audio/common_voice_it_42329444.wav",
    "common_voice_it_42329444": "audio/common_voice_it_42329484.wav",
    "common_voice_it_42686220": "audio/common_voice_it_42686220.wav",
    "rich": "audio/rich.wav",
}

class CoquiTTSProvider(TTSProvider):
    _instance = None

    def __init__(self):
        if not hasattr(self, "_tts"):
            self._tts = TTS(
                model_name="tts_models/multilingual/multi-dataset/xtts_v2",
                progress_bar=False,
                gpu=False
            )

    def synthesize(self, text: str, speaker: str, output_path: str) -> str:
        speaker_wav = COQUI_SPEAKERS.get(speaker)
        if not speaker_wav:
            raise ValueError(f"Unknown Coqui speaker: {speaker}")
        self._tts.tts_to_file(
            text=text,
            file_path=output_path,
            speaker_wav=speaker_wav,
            language="it"
        )
        return output_path
    
    def get_available_speakers(self) -> List[str]:
        return list(COQUI_SPEAKERS.keys())

    @classmethod
    def get_instance(cls) -> "CoquiTTSProvider":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
