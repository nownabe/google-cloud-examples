variable "project_id" {
  type = string
}
variable "region" {
  type    = string
  default = "asia-northeast1"
}

terraform {
  required_version = "~> 1.3.8"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.52.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

data "google_project" "project" {
  project_id = var.project_id
}
