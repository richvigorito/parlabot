package storage

import (
    "context"
    "os"
    "fmt"
    "cloud.google.com/go/storage"
    "google.golang.org/api/option"
)

func Make() (Storage, error) {
    driver := os.Getenv("STORAGE_DRIVER")
    switch driver {
        case "gcs":
            fmt.Println("Using GCS Storage Driver")
            //client, err := storage.NewClient(context.Background())
            client, err := createGCSClient(context.Background()) 

            if err != nil {
                fmt.Println("Error creating GCS client:", err)
                return nil, err
            }
            if os.Getenv("GCS_BUCKET") == "" {
                fmt.Println("GCS_BUCKET environment variable is not set")
                return nil, os.ErrInvalid
            }
            return &GCSStorage{
                BucketName: os.Getenv("GCS_BUCKET"),
                Client:     client,
            }, nil
        default:
            fmt.Println("Using Local Storage Driver")
            if os.Getenv("PUBLIC_URL") == "" {
                return nil, os.ErrInvalid
            }   

            s := &LocalStorage{
                BasePath:  "/app/shared/audio",
                PublicURL: os.Getenv("PUBLIC_URL")+ "/files",
                //PublicURL: "http://localhost:8000/files",
            }
            fmt.Println("public url ", s.PublicURL)
            fmt.Println("base path ", s.BasePath)
            return s, nil
    }
}

func createGCSClient(ctx context.Context) (*storage.Client, error) {
    credPath := os.Getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credPath != "" {
        fmt.Println("Using explicit credentials file from GOOGLE_APPLICATION_CREDENTIALS:", credPath)

        // Check that the file actually exists to avoid cryptic errors
        if _, err := os.Stat(credPath); os.IsNotExist(err) {
            fmt.Println("Credential file does not exist at path:", credPath)
            return nil, err
        }

        return storage.NewClient(ctx, option.WithCredentialsFile(credPath))
    }

    fmt.Println("Using Application Default Credentials (ADC)")
    return storage.NewClient(ctx)
}
