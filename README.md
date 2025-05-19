# ☕ ParlaBot: potrebbe ripeterlo?  
<em> (SpeakBot: Could you repeat that?) </em>

ParlaBot is a voice-enabled app that provides real-time feedback on your Italian pronunciation. Speak into your mic, and ParlaBot will transcribe what you said, compare it to a target phrase, and give constructive feedback — all powered by modern open-source AI.

---


### A Nod to the Past
My first real speech recognition project was my 2007 Master’s thesis — a vowel recognition frontend built with [FFTs](https://en.wikipedia.org/wiki/Fast_Fourier_transform), [Mel filters](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum), and [CMU Sphinx](https://en.wikipedia.org/wiki/CMU_Sphinx). It’s old-school compared to today’s AI toolkits, but this research (not necessarily mine, but those I studied) laid the foundation for the models that power ParlaBot.
[More on that here →](docs/ms.md)

### Fast-Forward to Now  
Nearly two decades later, I’ve been studying Italian seriously for three years and wanted to build something that merges:
- Revisited my past in speech recognition  
- Dips my toes into learning AI techniques (specific to STT)
- My passion for learning Italian  

Entrare il ParlaBot 
(Enter ParlaBot)

---

## Project Goals

- **Build a practical voice-powered Italian pronunciation coach**
- Showcase my ability to design, develop, and deploy AI-based microservices
- Reinforce my skills in Python, Go, C/C++, and microservice architecture
- Deliver a self-contained, demo-ready application in **under two weeks**

---

## Architecture Overview

ParlaBot is composed of several Dockerized microservices:

1. **Frontend API (FastAPI)**  
   - Exposes `/transcribe` to the frontend  
   - Orchestrates all service calls (STT, phrase, feedback)

2. **STT Service (Python + Transformers)**  
   - Uses Facebook's `wav2vec2-large-xlsr-53-italian` for transcription  
   - Accepts `.wav` audio and returns text

3. **Phrase Service (Go)**  
   - Returns a target Italian phrase (static or rotating)

4. **Feedback Service (C++)**  
   - Compares the user’s transcription with the target phrase  
   - Returns phonetic similarity or a rating (TBD)

5. **React Frontend**  
   - Records audio via browser  
   - Sends it to the backend and displays transcription + feedback

All services are containerized and connected via `docker-compose`.

---

## Tech Stack

- **Python**: FastAPI, Transformers, Torch, SoundFile  
- **Go**: REST microservice for phrase selection  
- **C++**: Feedback comparison engine (future enhancement)  
- **React**: Web UI with mic recording and feedback display  
- **Docker**: Multi-service deployment  

---

## How to Run

### 1. Clone the Repo
```bash
git clone https://github.com/richvigorito/parlabot.git
cd parlabot
```

### 2. Build and Run Services
```bash
docker-compose up --build
```

### 3. Start the Frontend
```bash
cd parlabot-client
npm install
npm start
```

### 4. Open in Browser  
Go to: [http://localhost:3000](http://localhost:3000)

---

## Roadmap

- [x] Speech-to-text service  
- [x] React frontend with mic recorder  
- [x] Feedback microservice design  
- [ ] Feedback microservice (C++ or Go)  
- [ ] Phrase database or spaced repetition deck  
- [ ] Support for voice playback and history  
- [ ] Deploy to cloud (Fly.io, DO, or AWS)

---

## License  
MIT License

---
## Author  
Rich Vigorito | Portland, OR | [LinkedIn](https://linkedin.com/in/rich-vigorito)  | [GitHub](https://github.com/richvigorito)
