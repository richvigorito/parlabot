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
- Deliver a self-contained, demo-ready application in **2–3 weeks**

---

## Architecture Overview

ParlaBot is composed of several Dockerized microservices:

1. **Frontend UI [React]**  
   - Displays the target phrase from the PhraseService  
   - Records mic input and sends audio to the Orchestrator  
   - Displays multiple transcriptions and feedback  

2. **API Orchestrator [Go (Gin)]**  
   - Exposes a `/transcribe` endpoint  
   - Forwards the user’s audio to multiple STT pipelines concurrently using goroutines  
   - (Planned) Routes results to the Feedback service  

3. **STT Service [Python (FastAPI) + HuggingFace Transformers + C++ Filters]**  
   - Accepts `.wav` audio  
   - Applies optional preprocessing via C++ filters  
   - Transcribes speech using `wav2vec2-large-xlsr-53-italian`  
   - Returns the model, preprocessing info, and transcript  

4. **Phrase Service [Python (FastAPI) + MongoDB + TTS]**  
   - Serves target phrases and audio  
   - (Planned) Tracks user progress  

5. **Feedback Service (TBD)**  
   - Compares STT output with the target phrase  
   - Returns phonetic or semantic similarity  

All services are containerized and connected via `docker-compose`.

```text
                        [ React UI  ]
                              |
                              v
                +------------------------------+
                |   Frontend API (Go / Gin)    | 
                | Receives audio, returns      |
                | feedback + transcriptions    |
                +------------------------------+
                       |         |        |
                       v         v        v
            +-------------+  +------------+  +------------------+
            |   STT Svc   |  | Feedback   |  | Phrase Service   |
            | (Python +   |  | (TBD)      |  | (Python + TTS)   |
            |  Wav2Vec2)  |  |            |  | Serves phrases   |
            +-------------+  +------------+  | & audio          |
                                             +------------------+
                       |
                       v
           +------------------------+
           | Audio Preprocessing    |
           | (C/C++ filter chain)   |
           +------------------------+
```

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

| Component         | Status       | Notes |
|------------------|--------------|-------|
| **React UI**      | ✅ Working     | Audio input, transcription display, waveforms/playback need refining |
| **Go API**        | ✅ Working     | Will be refactored as more STT pipelines and feedback are added |
| **STT Service**   | ✅ WIP         | Needs cleanup filters, support for more models |
| **Phrase Service**| ✅ Working     | Needs more sample phrases |
| **Feedback Svc**  | ❌ Not started| Will compute similarity between STT and target |
| **Kong**          | 🟡 Optional   | Would like to explore, not required |
| **Deployment**    | 🟡 Planning   | Targeting Fly.io, DO, or AWS |

---

## License  
MIT License

---

[Want to read this in Italian?](docs/README.it.md)

---
Rich Vigorito | Portland, OR | [LinkedIn](https://linkedin.com/in/rich-vigorito)  | [GitHub](https://github.com/richvigorito)
