package handlers

import (
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"

	"orchestrator/internal/http/resources"
	"orchestrator/internal/http/requests"

    "fmt"
)

// HandleTranscribe processes the multipart file inside the typed request
func HandleTranscribe(req requests.TranscribeRequest) ([]resources.TranscribeResponse, error) {
    fmt.Println("incoming req")
	fileHeader := req.File

	// Open the uploaded file
	file, err := fileHeader.Open()
	if err != nil {
		return nil, err
	}
	defer file.Close()
    fmt.Println("fileopened")

	// Save the uploaded file locally
	tempFilePath := filepath.Join(os.TempDir(), fileHeader.Filename)
	outFile, err := os.Create(tempFilePath)
	if err != nil {
		return nil, err
	}
	defer outFile.Close()
    fmt.Println("filesaved ... maybe dont do this tho")

	if _, err := io.Copy(outFile, file); err != nil {
		return nil, err
	}
    fmt.Println("copy bytes")

	// === New: Send the temp file to the STT service ===

	// Re-open temp file to send
	tempFile, err := os.Open(tempFilePath)
	if err != nil {
		return nil, err
	}
	defer tempFile.Close()
    
    fmt.Println("reopen tmp to send, seems redundant")

	var buf bytes.Buffer
	writer := multipart.NewWriter(&buf)

	formFile, err := writer.CreateFormFile("file", fileHeader.Filename)
	if err != nil {
		return nil, err
	}
    fmt.Println("create multipart form")

	if _, err := io.Copy(formFile, tempFile); err != nil {
		return nil, err
	}
    fmt.Println("copy to tmp (again?)")

	writer.Close()

	// Send to STT service
	resp, err := http.Post(
		"http://stt-service:5001/transcribe",
		writer.FormDataContentType(),
		&buf,
	)

	if err != nil {
		return nil, err
	}
   
    fmt.Println("Response status:", resp.Status) // e.g. "200 OK"
    bodyBytes, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, fmt.Errorf("reading response body: %w", err)
    }
    fmt.Println("Response body:", string(bodyBytes))

	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
        fmt.Println("bad status");
		return nil, errors.New("STT service failed")
	}

	var res resources.TranscribeResponse
    if err := json.Unmarshal(bodyBytes, &res); err != nil {
        fmt.Println("cannot decode", err);
		return nil, err
	}

    // IS this a leak? like i need to return the address?
    /// ie  return []resources.TranscribeResponse{&res}, nil ??
    fmt.Println("Return:", []resources.TranscribeResponse{res})
	return []resources.TranscribeResponse{res}, nil
}
