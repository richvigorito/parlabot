import yaml
import requests
import json
import re
import os
import sys
import subprocess
from google.cloud import texttospeech
from pathlib import Path

# CONFIG
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../keys/parlabot-adcf69150750.json"

PHRASE_API_ENDPOINT = "http://localhost:5002/phrases"  # /phrases POST endpoint
FILTER_API_BASE = "http://localhost:5002/filters"
LANGUAGE_CODE = "it-IT"
RAW_OUTPUT_DIR = "./out_audio/raw"
TRIMMED_OUTPUT_DIR = "./out_audio/trimmed"

# Initialize Google TTS client
client = texttospeech.TextToSpeechClient()

# Helper: safe filename
def safe_filename(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text[:50]

# Ensure output dirs exist
Path(RAW_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
Path(TRIMMED_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# ---- Parse CLI args ----
if len(sys.argv) < 3:
    print(f"Usage: python {sys.argv[0]} phrases.yaml save|upload [filter1 filter2 ...]")
    sys.exit(1)

yaml_file = sys.argv[1]
mode = sys.argv[2].lower()
ONLY_SAVE_FILES = True if mode == "save" else False
filters = sys.argv[3:]  # list of filters to run in order

print(f"Using YAML: {yaml_file}")
print(f"Mode: {'SAVE LOCALLY' if ONLY_SAVE_FILES else 'UPLOAD to phrase service'}")
print(f"Filters to apply: {filters if filters else 'None'}")

# ---- Load phrases ----
with open(yaml_file, "r") as f:
    phrases = yaml.safe_load(f)

# ---- Main loop ----
for phrase in phrases:
    print(f"\nProcessing: {phrase['text']}")

    for source in phrase["sources"]:
        print(f" - Source: {source['source_name']}, Speaker: {source['speaker']}")

        # Google TTS request
        synthesis_input = texttospeech.SynthesisInput(text=phrase["text"])
        voice = texttospeech.VoiceSelectionParams(
            language_code=LANGUAGE_CODE,
            name=source["speaker"]
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # Save raw MP3
        filename = f"{safe_filename(phrase['text'])}_{safe_filename(source['source_name'])}_{safe_filename(source['speaker'])}"
        raw_mp3_filepath = Path(RAW_OUTPUT_DIR) / f"{filename}.mp3"
        raw_wav_filepath = Path(RAW_OUTPUT_DIR) / f"{filename}.wav"

        with open(raw_mp3_filepath, "wb") as out:
            out.write(response.audio_content)

        # Convert MP3 → WAV using ffmpeg
        subprocess.run([
            "ffmpeg", "-y", "-i", str(raw_mp3_filepath),
            "-ar", "16000", "-ac", "1",
            str(raw_wav_filepath)
        ], check=True)

        print(f"Saved raw audio: {raw_wav_filepath}")

        # ---- Apply filters ----
        current_audio = raw_wav_filepath
        for filter_name in filters:
            print(f" Applying filter: {filter_name}")
            with open(current_audio, "rb") as f:
                r = requests.post(
                    f"{FILTER_API_BASE}/{filter_name}",
                    files={"audio_file": f}
                )

            if r.status_code != 200:
                print(f" Filter {filter_name} failed: {r.status_code} {r.text}")
                sys.exit(1)

            # Save intermediate result to trimmed dir
            current_audio = Path(TRIMMED_OUTPUT_DIR) / f"{filename}.{filter_name}.wav"
            with open(current_audio, "wb") as out:
                out.write(r.content)
            
            print(f"  Saved after {filter_name}: {current_audio}")

        # Final trimmed output is the last filter result, or raw WAV if no filters
        final_audio_path = current_audio if filters else raw_wav_filepath

        # Upload to phrase service if requested
        if not ONLY_SAVE_FILES:
            # Step 1: check if phrase already exists
            query_params = {"text": phrase["text"]}
            r = requests.get(PHRASE_API_ENDPOINT, params=query_params)

            if r.status_code == 404:
                # Phrase does not exist → create new one
                print("Phrase not found — creating new phrase")
                phrase_data = {
                    "level": phrase["level"],
                    "text": phrase["text"],
                    "translation": phrase.get("translation", ""),
                    "category": phrase.get("category", ""),
                }

                r2 = requests.post(PHRASE_API_ENDPOINT, json=phrase_data)
                if r2.status_code != 201:
                    print(f"Failed to create phrase: {r2.status_code} {r2.text}")
                    sys.exit(1)

                phrase_id = r2.json().get("id")
                print(f"Created new phrase with ID: {phrase_id}") 

            elif r.status_code == 200:
                phrase_id = r.json()[0]["id"]
                print(f"Phrase exists with ID: {phrase_id}")

            else:
                print(f"Unexpected response checking phrase: {r.status_code} {r.text}")
                sys.exit(1)
           
            ## step 3 create source
            source_data = {
                "source_name": source["source_name"],
                "speaker": source["speaker"]
            } 

            r3 = requests.patch(f"{PHRASE_API_ENDPOINT}/{phrase_id}/sources", json=sources)
            if r3.status_code != 201:
                print(f"Failed to create phrase source: {r3.status_code} {r3.text}")
                sys.exit(1)

            ## step 4 add audio to source
            sourc
            with open(final_audio_path, "rb") as f:
                r4 = requests.post(
                    f"{PHRASE_API_ENDPOINT}/{phrase_id}/sources/{source['source_name']/audio}",
                    files={"audio_file": f}
            )

            if r4.status_code == 201:
                print(f"Added new source to phrase {phrase_id}")
            else:
                print(f"Failed to add source: {r3.status_code} {r3.text}")
                sys.exit(1)
        
print("\nAll done.")

