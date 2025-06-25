import torchaudio
import io
from core.filters.base_filter import Filter

class TrimTrailingSilence(Filter):

    def __init__(self, threshold=0.01, padding_ms=500):
        self.threshold = threshold
        self.padding_ms = padding_ms

    def run_filter(self, audio_bytes: bytes) -> bytes:
        waveform, sample_rate = torchaudio.load(io.BytesIO(audio_bytes))
        initial_len = waveform.shape[1] / sample_rate

        trimmed_waveform = self.trim_trailing_silence(waveform, sample_rate)

        final_len = trimmed_waveform.shape[1] / sample_rate
        print(f"✅ Trimmed trailing silence: {initial_len:.2f}s → {final_len:.2f}s")

        buffer = io.BytesIO()
        torchaudio.save(buffer, trimmed_waveform, sample_rate=sample_rate, format="wav")
        buffer.seek(0)
        return buffer.getvalue()

    def trim_trailing_silence(self, waveform, sample_rate, threshold=0.01):
        frame_size = int(0.02 * sample_rate)  # 20ms frames
        hop_size = int(0.01 * sample_rate)    # 10ms hop

        energies = []
        for i in range(0, waveform.shape[1] - frame_size, hop_size):
            frame = waveform[:, i:i+frame_size]
            energy = frame.pow(2).mean().item()
            energies.append(energy)

        last_active_frame = 0
        for i, energy in enumerate(energies):
            if energy > threshold:
                last_active_frame = i


        padding_samples = int((self.padding_ms / 1000.0) * sample_rate)
        end_sample = min((last_active_frame + 1) * hop_size + padding_samples, waveform.shape[1])
      
        trimmed_waveform = waveform[:, :end_sample]
        return trimmed_waveform

