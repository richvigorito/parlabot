package main

import (
    "log"
    "orchestrator/internal/services"
    "orchestrator/internal/http/handlers"
    "orchestrator/internal/clients"
    "orchestrator/internal/storage"
    "github.com/gin-contrib/cors"
    "github.com/gin-gonic/gin"
    "time"
    "fmt"
    "os"
)

func main() {
    f, err := os.Create("/tmp/orchestrator.log")
    if err != nil {
        panic(err)
    }
    defer f.Close()

    log.SetOutput(f)
    fmt.Println("👀 starting orchestrator log")

    fmt.Println("entering main!")

    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }
    port = ":" + port
    fmt.Printf("Listening on port %s...", port)

    preprocessURL := os.Getenv("PREPROCESS_URL")
    if preprocessURL == "" {
	    fmt.Println("Missing PREPROCESS_URL env var")
	    log.Fatal("Missing PREPROCESS_URL env var")
    }
    fmt.Println("Preprocess URL:", preprocessURL)

    sttURL := os.Getenv("STT_URL")
    if sttURL == "" {
	    fmt.Println("Missing STT_URL env var")
	    log.Fatal("Missing STT_URL env var")
    }
    fmt.Println("STT URL:", sttURL)

    storage, err := storage.Make()
    if err != nil {
	    fmt.Println("Storage Driver Not Initialized", err)
	    log.Fatal("Storage Driver Not Initialized", err)
    }
    fmt.Println("Storage Driver Initialized")

    // Initialize services, clients and handlers
    preprocessingClient := clients.NewPreprocessingClient(preprocessURL)
    sttClient := clients.NewSTTClient(sttURL)
	transcriptionService := services.NewTranscriptionService(preprocessingClient, sttClient, storage)
    transcribeHandler := handlers.NewTranscribeHandler(transcriptionService)




    r := gin.Default()
    
    r.Use(cors.New(cors.Config{
        AllowOrigins:     []string{"http://localhost:3000", "http://localhost:5183", "https://parlabot.io", "https://frontend-ui-219914644880.us-central1.run.app/"}, // your UI origins
        AllowMethods:     []string{"POST", "GET", "OPTIONS"},
        AllowHeaders:     []string{"Origin", "Content-Type", "Accept"},
        ExposeHeaders:    []string{"Content-Length"},
        AllowCredentials: true,
        MaxAge:           12 * time.Hour,
    }))


    r.GET("/files/*filename", storage.HTTPHandler())

    apiGroup := r.Group("/api")
    apiGroup.POST("/transcribe", transcribeHandler.HandleTranscribeMulti)

    if err := r.Run(port); err != nil {
        log.Fatalf("Failed to run server: %v", err)
    }
}

