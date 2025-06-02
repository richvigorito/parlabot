import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from logging_config import setup_logging
from api.routers.phrases import router as phrases_router

setup_logging()
logger = logging.getLogger("phrase-service")

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

# Routers
app.include_router(phrases_router)

@app.get("/health")
def health():
    return {"ok": True}

