package utils

import (
	"bytes"
	"fmt"
	"io"
	"mime/multipart"
	"os"
)

type FileData struct {
	Filename string
	Content  []byte
}

func CreateSingleFileMultipartForm(fieldName string, file FileData, fields ...map[string]string) (io.Reader, string, error) {

	var buf bytes.Buffer
	writer := multipart.NewWriter(&buf)

	// Add optional fields
	if len(fields) > 0 && fields[0] != nil {
        for key, value := range fields[0] {
            if err := writer.WriteField(key, value); err != nil {
                return nil, "", fmt.Errorf("failed to write field %s: %w", key, err)
            }
        }
    }	

	// Add file
	formFile, err := writer.CreateFormFile(fieldName, file.Filename)
	if err != nil {
		return nil, "", fmt.Errorf("failed to create form file %s: %w", fieldName, err)
	}
	if _, err := formFile.Write(file.Content); err != nil {
		return nil, "", fmt.Errorf("failed to write file content: %w", err)
	}

	if err := writer.Close(); err != nil {
		return nil, "", fmt.Errorf("failed to close multipart writer: %w", err)
	}

	return &buf, writer.FormDataContentType(), nil
}

func ReadFileFromPath(filePath string) ([]byte, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to open file %s: %w", filePath, err)
	}
	defer file.Close()

	content, err := io.ReadAll(file)
	if err != nil {
		return nil, fmt.Errorf("failed to read file content from %s: %w", filePath, err)
	}

	return content, nil
}
