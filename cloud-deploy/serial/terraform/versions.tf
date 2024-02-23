terraform {
  required_version = "~> 1.7.3"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.16.0"
    }
  }
}
