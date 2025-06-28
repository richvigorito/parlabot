package storage

import (
    "context"
    "fmt"
    "io"
    "net/http"
    "strings"
    "cloud.google.com/go/storage"
    "github.com/gin-gonic/gin"
)

type GCSStorage struct {
    BucketName string
    Client     *storage.Client
}

func (g *GCSStorage) SaveFile(filename string, data []byte) (string, error) {
    ctx := context.Background()
    wc := g.Client.Bucket(g.BucketName).Object(filename).NewWriter(ctx)
    defer wc.Close()

    _, err := wc.Write(data)
    return fmt.Sprintf("gs://%s/%s", g.BucketName, filename), err
}

func (g *GCSStorage) GetFile(path string) ([]byte, error) {
    ctx := context.Background()
    reader, err := g.Client.Bucket(g.BucketName).Object(path).NewReader(ctx)
    if err != nil {
        return nil, err
    }
    defer reader.Close()
    return io.ReadAll(reader)
}

func (s *GCSStorage) HTTPHandler() gin.HandlerFunc {
    fmt.Println("Setting up GCS HTTP handler")
    return func(c *gin.Context) {
        filename := strings.TrimPrefix(c.Param("filename"), "/") // ✅ strip leading slash
        fmt.Println("GCS Fetching File:", filename)

        data, err := s.GetFile(filename)
        url := s.GetURL(filename)

        if err != nil {
            c.JSON(http.StatusNotFound, gin.H{
                "error":    "file not found",
                "message":  err.Error(),
                "filename": filename,
                "url":      url,
            })
            return
        }

        c.Data(http.StatusOK, "audio/wav", data)
    }
}


func (g *GCSStorage) GetURL(path string) string {
    // Remove any leading slash from the path
    cleanedPath := strings.TrimLeft(path, "/")
    return fmt.Sprintf("https://storage.googleapis.com/%s/%s", g.BucketName, cleanedPath)
} 

