import os
from asgi_correlation_id import correlation_id
import logging

SHARED_VOLUME_PATH = "/app/shared/"
logger = logging.getLogger("stt-service")

class AudioIO:
    @staticmethod
    def write_audio_file(path: str, data: bytes):
        with open(path, "wb") as f:
            f.write(data)

    @staticmethod
    def get_write_path(filename: str) -> str:
        cid = correlation_id.get() or "_nocid_"
        path = f"{cid}.{filename}"
        full_path = os.path.join(SHARED_VOLUME_PATH, path)
        logger.info(f"Write path: {full_path}")
        return full_path
