import torchaudio
import torchaudio.transforms as T
import io
from core.filters.base_filter import Filter

class Amplify(Filter):
    def __init__(self, gain_db=10.0):
        self.gain_db = gain_db

    def run_filter(self, audio_bytes: bytes) -> bytes:
        waveform, sample_rate = torchaudio.load(io.BytesIO(audio_bytes))
        waveform = T.Vol(self.gain_db, gain_type='amplitude')(waveform)

        buffer = io.BytesIO()
        torchaudio.save(buffer, waveform, sample_rate=sample_rate, format="wav")
        buffer.seek(0)
        return buffer.getvalue()
