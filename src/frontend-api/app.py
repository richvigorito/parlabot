from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# CORS setup for local dev with React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Placeholder for audio upload
@app.post("/api/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    # Save or process file here
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "transcription": "This is a fake transcription (replace me!)"
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
