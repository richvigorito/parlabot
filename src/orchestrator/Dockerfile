# ---- Build stage ----
##FROM golang:1.24 as builder
FROM golang:1.24-alpine AS builder

WORKDIR /app

# Copy go mod files and download deps first (better caching)
COPY go.mod go.sum ./
RUN go mod download

# Copy the rest of the app
COPY . .

# Build the binary
RUN go build -o orchestrator ./cmd/orchestrator

# ---- Run stage ----
FROM alpine:latest

WORKDIR /app

COPY --from=builder /app/orchestrator .

# Debug: check if the binary is present and permissions
RUN ls -lh /app

EXPOSE 8000

CMD ["./orchestrator"]
