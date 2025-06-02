from abc import ABC, abstractmethod

class Filter(ABC):
    @abstractmethod
    def run_filter(self, audio_bytes: bytes) -> bytes:
        """
        Run the filter on raw audio bytes.
        Returns processed audio bytes.
        """
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__

