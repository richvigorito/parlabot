# tts/google_tts.py
from services.tts.base import TTSProvider
from google.cloud import texttospeech
from typing import List

GOOGLE_SPEAKERS = [
    # "it-IT-Wavenet-A",
    # "it-IT-Wavenet-B",
    "it-IT-Standard-C"
]

class GoogleTTSProvider(TTSProvider):
    def synthesize(self, text: str, speaker: str, output_path: str) -> str:
        if speaker not in GOOGLE_SPEAKERS:
            raise ValueError(f"Unknown Google speaker: {speaker}")

        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="it-IT", name=speaker
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        with open(output_path, "wb") as out:
            out.write(response.audio_content)

        return output_path
    
    def get_available_speakers(self) -> List[str]:
        return GOOGLE_SPEAKERS
