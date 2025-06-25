import torchaudio
import torchaudio.functional as F
import io
from core.filters.base_filter import Filter

class BandPassFilter(Filter):
    def __init__(self, low_freq=300.0, high_freq=3400.0):
        self.low_freq = low_freq
        self.high_freq = high_freq

    def run_filter(self, audio_bytes: bytes) -> bytes:
        waveform, sample_rate = torchaudio.load(io.BytesIO(audio_bytes))
        
        filtered = F.bandpass_biquad(
            waveform,
            sample_rate=sample_rate,
            central_freq=(self.low_freq + self.high_freq) / 2,
            Q=sample_rate / (self.high_freq - self.low_freq)
        )

        buffer = io.BytesIO()
        torchaudio.save(buffer, filtered, sample_rate=sample_rate, format="wav")
        buffer.seek(0)
        return buffer.getvalue()
