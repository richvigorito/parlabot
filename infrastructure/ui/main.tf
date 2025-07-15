provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_cloud_run_service" "ui" {
  name     = "frontend-ui"
  location = var.region

  template {
    spec {
      containers {
        image = var.image
        # If your app exposes a port other than 8080, uncomment this and set it:
        # ports {
        #   container_port = 3000
        # }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  autogenerate_revision_name = true
}

resource "google_cloud_run_service_iam_member" "public_invoker" {
  service  = google_cloud_run_service.ui.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}

