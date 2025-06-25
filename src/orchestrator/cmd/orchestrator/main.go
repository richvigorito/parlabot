package main

import (
    "log"
    //"orchestrator/internal/http/api"
    "orchestrator/internal/services"
    "orchestrator/internal/http/handlers"
    "orchestrator/internal/clients"

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

    fmt.Println("entering main")

    // Initialize services, clients and handlers
	preprocessingClient := clients.NewPreprocessingClient("http://audio-preprocessing-service:5003")
	sttClient := clients.NewSTTClient("http://stt-service:5001")
	transcriptionService := services.NewTranscriptionService(preprocessingClient, sttClient)
    transcribeHandler := handlers.NewTranscribeHandler(transcriptionService)


    r := gin.Default()
    
    r.Use(cors.New(cors.Config{
        AllowOrigins:     []string{"http://localhost:3000", "http://localhost:5183"}, // your UI origins
        AllowMethods:     []string{"POST", "GET", "OPTIONS"},
        AllowHeaders:     []string{"Origin", "Content-Type", "Accept"},
        ExposeHeaders:    []string{"Content-Length"},
        AllowCredentials: true,
        MaxAge:           12 * time.Hour,
    }))


    // api.RegisterRoutes(r)
    r.Static("/files", "/app/shared")
    apiGroup := r.Group("/api")
    apiGroup.POST("/transcribe", transcribeHandler.HandleTranscribeMulti)

    if err := r.Run(":8000"); err != nil {
        log.Fatalf("Failed to run server: %v", err)
    }
}

