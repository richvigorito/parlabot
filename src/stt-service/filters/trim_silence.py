import torchaudio
import torchaudio.transforms as T
import io
from filters.base_filter import Filter

class TrimSilence(Filter):
    def run_filter(self, audio_bytes: bytes) -> bytes:
        waveform, sample_rate = torchaudio.load(io.BytesIO(audio_bytes))
        initial_len = waveform.shape[1] / sample_rate

        # Apply VAD (pytorch's voice activity detection)https://canonical.com/careers/6401160 
        trimmed_waveform = torchaudio.functional.vad(waveform, sample_rate=sample_rate)
        final_len = trimmed_waveform.shape[1] / sample_rate

        # If trimmed is empty, fallback to original
        if trimmed_waveform.shape[1] == 0:
            print(f"🟡 VAD removed everything. Keeping original {initial_len:.2f}s audio.")
            trimmed_waveform = waveform
            final_len = initial_len

        else:
            print(f"✅ Trimmed from {initial_len:.2f}s to {final_len:.2f}s")

        # Write result to buffer
        buffer = io.BytesIO()
        torchaudio.save(buffer, trimmed_waveform, sample_rate=sample_rate, format="wav")
        buffer.seek(0)
        return buffer.getvalue()

