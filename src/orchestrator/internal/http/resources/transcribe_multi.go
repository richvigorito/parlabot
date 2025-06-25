package resources

type TranscribeMultiResponse struct {
    InputFile       string  `json:"input_file"`
    Pipeline        string  `json:"pipeline"`
    Filters         []*FilterTransformationResponse `json:"transformations"`
    OutputFile      string  `json:"output_file"`
    Transcription   string  `json:"transcription"`
    Confidence      float64 `json:"confidence,omitempty"`
}

