import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from db.mongo import collection

from config import settings
from logging_config import setup_logging
from api.routers.phrases import router as phrases_router
from services.tts.coqui_tts import CoquiTTSProvider
import os


setup_logging()
logger = logging.getLogger("phrase-service")


logger.info("... Application startup beginning. init_tts underway")
try:
    CoquiTTSProvider.get_instance()
    logger.info("✅ init_tts complete")
except Exception as e:
    logger.info(f"❌ init_tts failed: {e}")
logger.info("🚀 Application startup complete — ready to serve requests!")



app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/audio", StaticFiles(directory=settings.AUDIO_DIR), name="audio")

@app.get("/health")
def health():
    logger.info("Health endpoint called")
    return {"ok": True}

# Routers
app.include_router(phrases_router)


