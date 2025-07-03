# Orchestrator

API Orchestrator in Go (Gin specifically)
   - Fetches all target phrases from the Phrase Service
   - Fetches all pipelines from the Audio Preprocessing Service
   - Exposes a `/transcribe` endpoint  
   - Concurrently via goroutines:
     - Forwards the user’s audio to each selected preprocessing pipeline  
     - Forwards the filtered audio to the STT Service for transcription and scoring
   - (Planned) Routes results to the Feedback service  
   -
   -
# Structure
```bash
.
├── cmd
│   └── orchestrator
│       └── main.go
├── Dockerfile
├── go.mod
├── go.sum
├── internal
│   ├── clients
│   │   ├── preprocessing_client.go
│   │   └── stt_client.go
│   ├── http
│   │   ├── api
│   │   ├── handlers
│   │   │   ├── transcribe.go
│   │   │   ├── transcribe_handler.go
│   │   │   └── transcribe_multi.go
│   │   ├── middleware
│   │   ├── requests
│   │   │   ├── transcribe.go
│   │   │   └── transcribe_multi.go
│   │   └── resources
│   │       ├── filterTransformation.go
│   │       ├── transcribe.go
│   │       └── transcribe_multi.go
│   ├── services
│   │   └── transcription_service.go
│   ├── storage
│   │   ├── gcs.go
│   │   ├── local.go
│   │   ├── storage_factory.go
│   │   └── storage.go
│   └── utils
│       └── multipart_utils.go
└── orchestrator
```

