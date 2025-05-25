# src/feedback-service/app.py or src/phrase-service/app.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Service is running"}
