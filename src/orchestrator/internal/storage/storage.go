package storage

import (
    "github.com/gin-gonic/gin"
)

type Storage interface {
    SaveFile(filename string, data []byte) (string, error)
    GetFile(path string) ([]byte, error)
    GetURL(path string) string
    HTTPHandler() gin.HandlerFunc
}
