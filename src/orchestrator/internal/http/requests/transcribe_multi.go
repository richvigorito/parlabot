package requests

import (
    "errors"
    "mime/multipart"

    "github.com/gin-gonic/gin"
)

type TranscribeMultiRequest struct {
    File *multipart.FileHeader
    Pipelines []string
}

func BindTranscribeMultiRequest(c *gin.Context) (TranscribeMultiRequest, error) {
    var req TranscribeMultiRequest

    file, err := c.FormFile("file")
    if err != nil {
        return req, errors.New("file is required")
    }

    pipelines := c.PostFormArray("pipelines")
    if len(pipelines) == 0 {
        return req, errors.New("at least one pipeline is required")
    }
    req.Pipelines = pipelines
    req.File = file

    return req, nil
}
