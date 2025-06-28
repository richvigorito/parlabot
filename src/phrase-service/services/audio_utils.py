import io
from uuid import uuid4
from storage.storage_factory import make_storage

storage = make_storage()

def generate_storage_path(prefix: str = "audio", ext: str = "wav") -> str:
    return f"{prefix}/{uuid4().hex}.{ext}"

async def save_audio_bytes(prefix: str, data: bytes, ext: str = "wav") -> str:
    path = generate_storage_path(prefix, ext)
    storage.save(path, data)
    return storage.public_url(path)

async def save_upload_file(prefix: str, file) -> str:
    contents = await file.read()
    return await save_audio_bytes(prefix, contents, ext=file.filename.split('.')[-1])

def synthesize_to_storage(provider, text: str, speaker: str, prefix: str = "tts") -> str:
    buffer = io.BytesIO()
    provider.synthesize(text=text, speaker=speaker, output_path=buffer)
    return storage.save_and_url(generate_storage_path(prefix), buffer.getvalue())

