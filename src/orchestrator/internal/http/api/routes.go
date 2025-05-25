//  orchestrator/internal/http/api/routes.go 

package api

import (
    "net/http"

    "github.com/gin-gonic/gin"
    "orchestrator/internal/http/handlers"
    "orchestrator/internal/http/requests"

    "fmt"
)

func RegisterRoutes(r *gin.Engine) {
    fmt.Println("registering routes")
  
    r.Static("/files", "/app/shared")

    api := r.Group("/api")

    api.POST("/transcribe", func(c *gin.Context) {
        fmt.Println("register api/transcribe")
        req, err := requests.BindTranscribeRequest(c)
        if err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }

        resp, err := handlers.HandleTranscribe(req)
        if err != nil {
            c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
            return
        }

        c.JSON(http.StatusOK, resp)
    })
}
