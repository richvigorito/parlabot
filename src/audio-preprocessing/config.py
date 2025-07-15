import os

class Settings:
    STORAGE_DRIVER = os.getenv("STORAGE_DRIVER", "local")  # or "gcs"
    GCS_BUCKET = os.getenv("GCS_BUCKET", "")  
    FILES_URL = os.getenv("FILES_URL", "http://localhost:8000/files")  
    AUDIO_DIR = "/app/shared/audio"

settings = Settings()

