import logging
from fastapi import FastAPI
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi.middleware.cors import CORSMiddleware
from logging_config import setup_logging
from api.routers.pipeline import router as pipeline_router
from api.routers.filter import router as filter_router

# Initialize logging
setup_logging()
logger = logging.getLogger("audio-preprocessor")

app = FastAPI()
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(filter_router)
app.include_router(pipeline_router)

@app.get("/health")
def health():
    logger.info("va bene")
    return {"ok": True}

