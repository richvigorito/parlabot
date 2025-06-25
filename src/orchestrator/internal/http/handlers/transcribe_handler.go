package handlers

import (
	"fmt"
	"net/http"
	//	"orchestrator/internal/http/resources"
	"orchestrator/internal/http/requests"
	"orchestrator/internal/services"
	
	"github.com/gin-gonic/gin"
)

type TranscribeHandler struct {
	transcriptionService *services.TranscriptionService
}

func NewTranscribeHandler(transcriptionService *services.TranscriptionService) *TranscribeHandler {
	return &TranscribeHandler{
		transcriptionService: transcriptionService,
	}
}

// HandleTranscribeMulti processes multi-pipeline transcription requests
func (h *TranscribeHandler) HandleTranscribeMulti(c *gin.Context) {
	// Bind and validate request
	req, err := requests.BindTranscribeMultiRequest(c)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	fmt.Printf("Processing transcription request with %d pipelines\n", len(req.Pipelines))

	responses, err := h.transcriptionService.ProcessMultiplePipelines(req)
	if err != nil {
		// You might want more sophisticated error handling here
		// (e.g., distinguish between client errors, server errors, partial failures)
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Return successful response
	c.JSON(http.StatusOK, gin.H{
		"results": responses,
		"count":   len(responses),
	})
}

// HandleTranscribeSingle - keeping the original single pipeline handler
func (h *TranscribeHandler) HandleTranscribeSingle(c *gin.Context) {
	req, err := requests.BindTranscribeRequest(c)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Convert single request to multi request with one pipeline
	multiReq := requests.TranscribeMultiRequest{
		File:      req.File,
		Pipelines: []string{"default"}, // or whatever your default pipeline is
	}

	responses, err := h.transcriptionService.ProcessMultiplePipelines(multiReq)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	if len(responses) == 0 {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "no results returned"})
		return
	}

	// Return single result for backward compatibility
	c.JSON(http.StatusOK, responses[0])
}
