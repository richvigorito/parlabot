package storage

import (
    "net/http"
    "os"
    "path/filepath"

    "github.com/gin-gonic/gin"
)

type LocalStorage struct {
    BasePath  string
    PublicURL string
}

func (l *LocalStorage) SaveFile(filename string, data []byte) (string, error) {
    fullPath := filepath.Join(l.BasePath, filename)
    err := os.WriteFile(fullPath, data, 0644)
    return fullPath, err
}

func (l *LocalStorage) GetFile(path string) ([]byte, error) {
    fullPath := filepath.Join(l.BasePath, path)
    return os.ReadFile(fullPath)
}

func (s *LocalStorage) HTTPHandler() gin.HandlerFunc {
    fs := gin.Dir(s.BasePath, false)
    return gin.WrapH(http.StripPrefix("/files/", http.FileServer(fs)))
}

func (l *LocalStorage) GetURL(path string) string {
    return l.PublicURL + "/" + path
}
