package resources

type TranscribeResponse struct {
    InputFile       string  `json:"input_file"`
    Filters         []*FilterTransformationResponse `json:"transformations"`
    OutputFile      string  `json:"output_file"`
    Transcription   string  `json:"transcription"`
    Confidence      float64 `json:"confidence,omitempty"`
}

