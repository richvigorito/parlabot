import logging
from fastapi import FastAPI
from asgi_correlation_id import CorrelationIdMiddleware
from logging_config import setup_logging
from api.routers.transcribe import router as transcribe_router
from api.routers.filter import router as filter_router

# Initialize logging
setup_logging()
logger = logging.getLogger("stt-service")

app = FastAPI()
app.add_middleware(CorrelationIdMiddleware)

app.include_router(transcribe_router)
app.include_router(filter_router)

@app.get("/health")
def health():
    return {"ok": True}

