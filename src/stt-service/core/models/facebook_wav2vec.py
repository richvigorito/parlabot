# core/models/facebook_wav2vec.py
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from core.models.base_model import Transcriber

class FacebookWav2vec2LargeXslr53Italian(Transcriber):
    def __init__(self):
        self.processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-xlsr-53-italian")
        self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53-italian")

    def process(self, waveform: torch.Tensor) -> tuple[str, float]:
        input_values = self.processor(
            waveform.squeeze().numpy(),
            sampling_rate=16000,
            return_tensors="pt",
            padding="longest"
        ).input_values

        with torch.no_grad():
            logits = self.model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0].lower()
        # TODO: Add real confidence logic sometime later
        return transcription, 0.9
