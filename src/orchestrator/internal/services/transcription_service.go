package services

import (
	"fmt"
	"io"
	//"os"
	"mime/multipart"
	"strings"
	//"net/http"
	"sync"

	"orchestrator/internal/clients"
 	"orchestrator/internal/http/resources"
	"orchestrator/internal/http/requests"
    "orchestrator/internal/storage"
)

type TranscriptionService struct {
	preprocessingClient *clients.PreprocessingClient
	sttClient           *clients.STTClient
	storage           	storage.Storage
}

func NewTranscriptionService(preprocessingClient *clients.PreprocessingClient, sttClient *clients.STTClient, storage storage.Storage) *TranscriptionService {
	return &TranscriptionService{
		preprocessingClient: preprocessingClient,
		sttClient:           sttClient,
		storage:           	 storage,
	}
}

type PipelineResult struct {
	Pipeline string                              `json:"pipeline"`
	Response *resources.TranscribeMultiResponse `json:"response,omitempty"`
	Error    string                             `json:"error,omitempty"`
}

func (s *TranscriptionService) ProcessMultiplePipelines(req requests.TranscribeMultiRequest) ([]resources.TranscribeMultiResponse, error) {
	fileContent, err := s.readFileContent(req.File)
	if err != nil {
		return nil, fmt.Errorf("failed to read file content: %w", err)
	}

	results := make(chan PipelineResult, len(req.Pipelines))
	var wg sync.WaitGroup

	for _, pipeline := range req.Pipelines {
		wg.Add(1)
		go func(pipelineName string) {
			defer wg.Done()
			results <- s.processSinglePipeline(pipelineName, req.File.Filename, fileContent)
		}(pipeline)
	}

	go func() {
		wg.Wait()
		close(results)
	}()

	return s.collectResults(results, len(req.Pipelines))
}

func (s *TranscriptionService) readFileContent(fileHeader *multipart.FileHeader) ([]byte, error) {
	file, err := fileHeader.Open()
	if err != nil {
		return nil, err
	}
	defer file.Close()
	return io.ReadAll(file)
}

func (s *TranscriptionService) processSinglePipeline(pipeline, filename string, fileContent []byte) PipelineResult {
	preprocessResponse, err := s.preprocessingClient.ProcessFile(pipeline, filename, fileContent)
	if err != nil {
		return PipelineResult{Pipeline: pipeline, Error: fmt.Sprintf("preprocessing failed: %v", err)}
	}

	fmt.Printf("Pipeline %s processed file: %s -> %s\n", pipeline, preprocessResponse.InputFile, preprocessResponse.OutputFile)	

	// url := fmt.Sprintf("%s%s", s.preprocessingClient.BaseURL(), preprocessResponse.OutputFile)
	// resp, err := http.Get(url)
	//if err != nil {
		//return PipelineResult{Pipeline: pipeline, Error: fmt.Sprintf("failed to fetch processed file: %v", err)}
	// }
	// defer resp.Body.Close()
	//if resp.StatusCode != http.StatusOK {
		//return PipelineResult{Pipeline: pipeline, Error: fmt.Sprintf("fetch failed: status %d", resp.StatusCode)}
	//}
	//processedContent, err := io.ReadAll(resp.Body)
	// replace 'files' with emtpy
	//processedPath := "/app/shared" +  


	//processedPath := "/app/shared" + strings.Replace(preprocessResponse.OutputFile, "/files", "", 1)  
	//fmt.Printf("Processed file path: %s\n", processedPath)
	//processedContent, err := os.ReadFile(processedPath)

	objectPath := strings.TrimPrefix(preprocessResponse.OutputFile, "/files/")
	processedContent, err := s.storage.GetFile(objectPath)
	if err != nil {
		fmt.Printf("Failed to read processed file for pipeline %s: %v\n", pipeline, err)
		return PipelineResult{Pipeline: pipeline, Error: fmt.Sprintf("read error: %v", err)}
	}
	fmt.Printf("Processed content length: %d bytes\n", len(processedContent))

	// transcription, confidence, err := s.sttClient.TranscribeFile(processedContent, filename)
	transcriptionResponse, err := s.sttClient.TranscribeFile(filename, processedContent)
	if err != nil {
		fmt.Printf("Transcription failed for pipeline %s: %v\n", pipeline, err)
		return PipelineResult{Pipeline: pipeline, Error: fmt.Sprintf("STT failed: %v", err)}
	}
	fmt.Printf("Transcription for pipeline %s: %s (confidence: %.2f)\n", pipeline, transcriptionResponse.Transcription, transcriptionResponse.Confidence)

	return PipelineResult{
		Pipeline: pipeline,
		Response: &resources.TranscribeMultiResponse{
			InputFile:     preprocessResponse.InputFile,
			Pipeline:      pipeline,
			Filters:       preprocessResponse.Filters,
			OutputFile:    preprocessResponse.OutputFile,
			Transcription: transcriptionResponse.Transcription,
			Confidence:    transcriptionResponse.Confidence,
		},
	}
}

func (s *TranscriptionService) collectResults(results chan PipelineResult, expectedCount int) ([]resources.TranscribeMultiResponse, error) {
	var responses []resources.TranscribeMultiResponse
	var errors []string

	for result := range results {
		if result.Error != "" {
			errors = append(errors, fmt.Sprintf("%s: %s", result.Pipeline, result.Error))
		} else if result.Response != nil {
			responses = append(responses, *result.Response)
		}
	}

	if len(responses) == 0 {
		return nil, fmt.Errorf("all pipelines failed: %v", errors)
	}
	return responses, nil
}
