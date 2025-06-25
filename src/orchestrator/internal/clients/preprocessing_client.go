package clients

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"orchestrator/internal/http/resources"
	"orchestrator/internal/utils"
)

type PreprocessingClient struct {
	baseURL    string
	httpClient *http.Client
}

func NewPreprocessingClient(baseURL string) *PreprocessingClient {
	return &PreprocessingClient{
		baseURL:    baseURL,
		httpClient: &http.Client{},
	}
}

type PreprocessResponse struct {
	InputFile  string                                    `json:"input_file"`
	OutputFile string                                    `json:"output_file"`
	Filters    []*resources.FilterTransformationResponse `json:"transformations"`
}

// ProcessFile sends the file to the preprocessing pipeline
func (c *PreprocessingClient) ProcessFile(pipeline, filename string, fileContent []byte) (*PreprocessResponse, error) {
	body, contentType, err := utils.CreateSingleFileMultipartForm(
		"file",
		utils.FileData{
			Filename: filename,
			Content:  fileContent,
		},
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create multipart form: %w", err)
	}

	url := fmt.Sprintf("%s/pipelines/%s/run", c.baseURL, pipeline)
	resp, err := c.httpClient.Post(url, contentType, body)
	if err != nil {
		return nil, fmt.Errorf("failed to call preprocessing service: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		bodyBytes, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("preprocessing service returned status %d: %s",
			resp.StatusCode, string(bodyBytes))
	}

	var preprocessResponse PreprocessResponse
	if err := json.NewDecoder(resp.Body).Decode(&preprocessResponse); err != nil {
		return nil, fmt.Errorf("failed to decode preprocessing response: %w", err)
	}

	return &preprocessResponse, nil
}

func (c *PreprocessingClient) BaseURL() string {
	return c.baseURL
}

