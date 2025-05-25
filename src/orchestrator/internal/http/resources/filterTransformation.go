package resources

type FilterTransformationResponse struct {
    FilterName  string                  `json:"filter_name"`
    InputFile   string                  `json:"input_file"`
    OutputFile  string                  `json:"output_file"`
    Metadata    map[string]interface{}  `json:"metadata,omitempty"`
}

