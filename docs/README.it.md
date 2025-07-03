# ☕ ParlaBot: potrebbe ripeterlo?  

ParlaBot è un'applicazione abilitata alla voce che ti fornisce feedback in tempo reale sulla tua pronuncia italiana. Parla nel microfono e ParlaBot trascriverà ciò che hai detto, lo confronterà con una frase di riferimento e fornirà feedback costruttivo, il tutto alimentato da moderne tecnologie AI open-source e tecniche tradizionali di filtraggio DSP.

--- 

### Prima, un Riconoscimento al Passato

Il mio primo vero progetto di riconoscimento vocale è stata la mia tesi di Master del 2007: un frontend di riconoscimento delle vocali costruito utilizzando [FFTs](https://en.wikipedia.org/wiki/Fast_Fourier_transform), [filtri Mel](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum) e [CMU Sphinx](https://en.wikipedia.org/wiki/CMU_Sphinx). È vecchio stile rispetto agli attuali toolkit AI, ma questa ricerca (non necessariamente la mia, ma quella che ho studiato) ha gettato le basi per i modelli che alimentano ParlaBot.
[Si può leggere di più qui →](docs/ms.md)

---
### Avanti Veloce fino a Oggi

Quasi due decenni dopo, ho studiato seriamente l'italiano per tre anni e volevo costruire qualcosa che unisse:

- La rivisitazione dei miei studi passati nel riconoscimento vocale
- Esplorazione pratica dei moderni toolkit STT e AI
- La mia passione per l'apprendimento dell'italiano

--- 
### Obiettivi del Progetto
- Costruire un pratico coach di pronuncia italiana abilitato alla voce  
- Mostrare la mia capacità di progettare, sviluppare e distribuire microservizi basati su AI
- Rafforzare le competenze in Python, Go, C/C++ e architettura basata su container


---
### Panoramica dell'Architettura
ParlaBot è composto da diversi microservizi Dockerizzati:
1. [Frontend UI](/src/frontend-ui) in React
   - Mostra la frase di riferimento dal PhraseService
   - Registra l'input del microfono e invia l'audio all'Orchestrator
   - Mostra più trascrizioni e feedback

2. [API Orchestrator](/src/orchestrator) in Go/Gin
    - Recupera tutte le frasi di riferimento dal Phrase Service
    - Recupera tutte le pipeline dal Servizio di Pre-elaborazione Audio
    - Espone un endpoint `/transcribe`
    - In modo concorrente tramite goroutine:
      - Inoltra l'audio dell'utente a ciascuna pipeline di pre-elaborazione selezionata
      - Inoltra l'audio filtrato al Servizio STT per la trascrizione e la valutazione
    - (Pianificato) Instrada i risultati al servizio Feedback
3. [Servizio di Pre-elaborazione Audio](/src/audio-preprocessing) in Python/FastAPI + Torch Transformers
    - Accetta audio in formato `.wav`
    - Esegue l'audio attraverso pipeline di pre-elaborazione specificate
    - (Pianificato) Consuma/integrerà oggetti condivisi C++ compilati per catene di filtri audio dal registro
4. [Servizio STT](/src/stt-service) in Python/FastAPI + Trascrittori di Modelli Linguistici HuggingFace
    - Accetta audio filtrato in formato `.wav`
    - Esegue la trascrizione e la valutazione dell'audio filtrato
    - (Pianificato) Inoltra i risultati al servizio Feedback
5. [Servizio Phrase](/src/phrase-service) in Python/FastAPI
    - Accetta richieste per frasi di riferimentoA

---
Rich Vigorito | Portland, OR | [LinkedIn](https://linkedin.com/in/rich-vigorito)  | [GitHub](https://github.com/richvigorito)
