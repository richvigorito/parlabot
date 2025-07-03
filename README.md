# ☕ ParlaBot: potrebbe ripeterlo?  
<em>(SpeakBot: Could you repeat that?)</em>

ParlaBot is a voice-enabled app that gives you real-time feedback on your Italian pronunciation. Speak into your mic, and ParlaBot will transcribe what you said, compare it to a target phrase, and return constructive feedback — powered by modern open-source AI and traditional DSP filtering techniques.

---

### First, a Nod to the Past

My first real speech recognition project was my 2007 Master’s thesis — a vowel recognition frontend built using [FFTs](https://en.wikipedia.org/wiki/Fast_Fourier_transform), [Mel filters](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum), and [CMU Sphinx](https://en.wikipedia.org/wiki/CMU_Sphinx). It’s old-school compared to today’s AI toolkits, but this research (not necessarily mine, but those I studied) laid the foundation for the models that power ParlaBot.  
[More on that here →](docs/ms.md)

---

### Fast-Forward to Now

Nearly two decades later, I’ve been studying Italian seriously for three years and wanted to build something that merges:

- Revisiting of my past studies in speech recognition  
- Hands-on exploration of modern STT and AI toolkits  
- My passion for learning Italian  

**Entrare il ParlaBot**  
(*Enter ParlaBot*)

---

## Project Goals

- Build a practical voice-powered Italian pronunciation coach  
- Showcase my ability to design, develop, and deploy AI-based microservices  
- Reinforce skills in Python, Go, C/C++, and container-based architecture  

---

## Architecture Overview

ParlaBot is composed of several Dockerized microservices:

1. [Frontend UI](/src/front-ui) in React
   - Displays the target phrase from the PhraseService  
   - Records mic input and sends audio to the Orchestrator  
   - Displays multiple transcriptions and feedback  

2. [API Orchestrator](/src/orchestrator) in Go/Gin
   - Fetches all target phrases from the Phrase Service
   - Fetches all pipelines from the Audio Preprocessing Service
   - Exposes a `/transcribe` endpoint  
   - Concurrently via goroutines:
     - Forwards the user’s audio to each selected preprocessing pipeline  
     - Forwards the filtered audio to the STT Service for transcription and scoring
   - (Planned) Routes results to the Feedback service  

3. [Audio Preprocessing Service](/src/audio-preprocessing) in Python/FastAPI + Torch Transformers 
   - Accepts `.wav` audio  
   - Runs audio through specified preprocessing pipelines
   - (Planned) Consume/integrate compoiled C++ shared objects filter chains for audio preprocessing from registry

3. [STT Service](/src/stt-service) in Python/FastAPI + HuggingFace Language Model Transcribers
   - Accepts filtered `.wav` audio  
   - Transcribes speech using language model, currently only supports `wav2vec2-large-xlsr-53-italian` 
   - Scores the transcription against the target phrase
   - Returns the model, preprocessing info, and transcript  
   - (Planned) Add support for multiple models  

4. [Phrase Service](/src/phrase-service) in Python/FastAPI + MongoDB + coqui (with mozilla and personal speaker training files)  + Google TTS API
   - Accepts text phrases and TTS speaker and generates audio using TTS
   - (Planned) Tracks user progress  


All services are containerized and connected via `docker-compose`.

## Current System Architecture

<p align="center">
  <img src="/assets/system.current.png"  width="600"/>
</p>

[... Where its going](/assets/system.future.png)

---

## How to Run

```bash
git clone https://github.com/richvigorito/parlabot.git
cd parlabot
docker-compose up --build
open http://localhost:3000
```

---

## Roadmap
see [milestones](/milestones) for project milestones/roadmaps/issues/etc

---

## License  
MIT License

---

[Want to read this in Italian?](docs/README.it.md)

---
Rich Vigorito | Portland, OR | [LinkedIn](https://linkedin.com/in/rich-vigorito)  | [GitHub](https://github.com/richvigorito)
