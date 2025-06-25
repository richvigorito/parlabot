# tts/provider_factory.py
from services.tts.coqui_tts import CoquiTTSProvider
from services.tts.google_tts import GoogleTTSProvider

PROVIDERS = {
    "coqui": CoquiTTSProvider(),
    "google": GoogleTTSProvider(),
}


def get_tts_provider(name: str):
    return PROVIDERS[name]

def build_provider_map() -> dict:
    return {
        name: provider.get_available_speakers()
        for name, provider in PROVIDERS.items()
    }

def build_provider_map_from_path(providers_speakers: str) -> dict:
    provider_map = {}

    for item in providers_speakers.split(","):
        parts = item.split(".")
        provider = parts[0]
        speaker = parts[1] if len(parts) > 1 else None
        provider_map.setdefault(provider, [])
        if speaker:
            provider_map[provider].append(speaker)

    for provider, speakers in provider_map.items():
        if not speakers:
            provider_map[provider] = PROVIDERS[provider].get_available_speakers()

    return provider_map
