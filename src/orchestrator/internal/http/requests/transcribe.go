package requests

import (
    "errors"
    "mime/multipart"

    "github.com/gin-gonic/gin"
)

type TranscribeRequest struct {
    File *multipart.FileHeader
}

func BindTranscribeRequest(c *gin.Context) (TranscribeRequest, error) {
    var req TranscribeRequest

    file, err := c.FormFile("file")
    if err != nil {
        return req, errors.New("file is required")
    }
    req.File = file

    return req, nil
}
