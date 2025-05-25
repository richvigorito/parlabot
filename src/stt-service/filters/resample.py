import torchaudio
import torch
import io
from filters.base_filter import Filter


class ResampleTo16k(Filter):
    def run_filter(self, audio_bytes: bytes) -> bytes:
        """
        Takes raw audio bytes and returns WAV bytes resampled to 16kHz mono.
        """
        # Load audio from bytes
        waveform, orig_sr = torchaudio.load(io.BytesIO(audio_bytes))

        # If stereo, convert to mono
        if waveform.shape[0] > 1:
            print(f"Converting to mono: {waveform.shape[0]} channels")
            waveform = waveform.mean(dim=0, keepdim=True)

        # Resample if needed
        if orig_sr != 16000:
            print(f"Resampling from {orig_sr} Hz to 16000 Hz")
            resampler = torchaudio.transforms.Resample(orig_sr, 16000)
            waveform = resampler(waveform)

        print(f"Final waveform shape: {waveform.shape}")

        # Save to bytes in WAV format
        buffer = io.BytesIO()
        torchaudio.save(buffer, waveform, 16000, format="wav")
        buffer.seek(0)
        return buffer.getvalue()

