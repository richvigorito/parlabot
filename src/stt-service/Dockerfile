FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg libsndfile1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python3 -c "from transformers import Wav2Vec2Processor; Wav2Vec2Processor.from_pretrained('facebook/wav2vec2-large-xlsr-53-italian')"

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
