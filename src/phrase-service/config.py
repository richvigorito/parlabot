import os

class Settings:
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
    DB_NAME = "phrases"
    COLLECTION_NAME = "italian"
    ## AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")
    AUDIO_DIR = "/app/shared/audio"
    SPEAKER = "/app/audio/common_voice_it_42329484.wav"

settings = Settings()

