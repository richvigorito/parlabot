# tts/base.py
from abc import ABC, abstractmethod
from typing import List

class TTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str, speaker: str, output_path: str) -> str:
        """Generate audio and return path or URL"""
        pass

    def get_available_speakers(self) -> List[str]:
        raise NotImplementedError

