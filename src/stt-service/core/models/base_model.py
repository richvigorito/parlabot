# core/models/base_model.py
from abc import ABC, abstractmethod
import torch

class Transcriber(ABC):

    @abstractmethod
    def process(self, waveform: torch.Tensor) -> tuple[str, float]:
        """
        Returns transcription and confidence score
        """
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__
