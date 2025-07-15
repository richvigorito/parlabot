from abc import ABC, abstractmethod
from asgi_correlation_id import correlation_id

class Storage(ABC):
    @abstractmethod
    def save_file(self, filename: str, data: bytes) -> str:
        pass

    @abstractmethod
    def get_url(self, path: str) -> str:
        pass

    def build_storage_path(self, step_idx: int, name: str, base_dir: str = "temp") -> str:
        print(f"Building storage path for step {step_idx}, name {name}, base_dir {base_dir}")
        cid = correlation_id.get() or "_nocid_"
        return f"{base_dir}/{cid}.step{step_idx}_{name}.wav"

    def save_and_url(self, path: str, data: bytes) -> str:
        self.save(path, data)
        return self.public_url(path)

