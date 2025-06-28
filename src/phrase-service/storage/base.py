from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save_file(self, filename: str, data: bytes) -> str:
        pass

    @abstractmethod
    def get_url(self, path: str) -> str:
        pass

    def save_and_url(self, path: str, data: bytes) -> str:
        self.save(path, data)
        return self.public_url(path)

