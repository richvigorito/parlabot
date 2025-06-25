package clients

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	// "path/filepath"
	"orchestrator/internal/utils"
)

type STTClient struct {
	baseURL    string
	httpClient *http.Client
}

func NewSTTClient(baseURL string) *STTClient {
	return &STTClient{
		baseURL:    baseURL,
		httpClient: &http.Client{},
	}
}

// STTResponse represents the response from the STT service
type STTResponse struct {
	Transcription string  `json:"transcription"`
	Confidence    float64 `json:"confidence"`
}

func (c *STTClient) TranscribeFile(filename string, fileContent []byte) (*STTResponse, error) {
	fmt.Printf("Transcribing file: %s\n", filename)
	body, contentType, err := utils.CreateSingleFileMultipartForm("file",	utils.FileData{
			Filename: filename,
			Content:  fileContent,
	})

	if err != nil {
		return nil, fmt.Errorf("failed to create multipart form: %w", err)
	}
	fmt.Printf("Sending transcription request for file: %s\n", filename)

	url := fmt.Sprintf("%s/transcribe", c.baseURL)
	resp, err := c.httpClient.Post(url, contentType, body)
	if err != nil {
		return nil, fmt.Errorf("failed to call STT service: %w", err)
	}
	defer resp.Body.Close()

	// Handle response
	if resp.StatusCode != http.StatusOK {
		bodyBytes, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("STT service returned status %d: %s", 
			resp.StatusCode, string(bodyBytes))
	}

	// Parse response
	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read STT response: %w", err)
	}

	var sttResponse STTResponse
	if err := json.Unmarshal(bodyBytes, &sttResponse); err != nil {
		return nil, fmt.Errorf("failed to decode STT response: %w", err)
	}

	fmt.Printf("STT completed for file %s: confidence %.2f\n", filename, sttResponse.Confidence)

	return &sttResponse, nil
}
