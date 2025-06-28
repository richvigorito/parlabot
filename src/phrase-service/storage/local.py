from .base import Storage
import os
from config import settings

class LocalStorage(Storage):
    def __init__(self, base_path=settings.AUDIO_DIR, public_url=settings.FILES_URL):
        self.base_path = base_path
        self.public_url = public_url

    def save_file(self, filename, data):
        full_path = os.path.join(self.base_path, filename)
        with open(full_path, "wb") as f:
            f.write(data)
        return full_path

    def get_url(self, path):
        return f"{self.public_url}/{path}"

