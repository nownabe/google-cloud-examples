// -------- projects -------- //
resource "google_project" "pipeline" {
  name            = "${var.project_prefix}-pipeline"
  project_id      = "${var.project_prefix}-pipeline"
  billing_account = data.google_billing_account.billing.id
}

resource "google_project_service" "artifactregistry" {
  project = google_project.pipeline.project_id
  service = "artifactregistry.googleapis.com"
}

resource "google_project_service" "clouddeploy" {
  project = google_project.pipeline.project_id
  service = "clouddeploy.googleapis.com"
}

//-------- hello-app-deployer Service Account --------//

# Service Account for creating Cloud Deploy Release.
# In other words, this Service Account will be used to trigger a delivery pipeline.
resource "google_service_account" "hello-app-deployer" {
  project      = google_project.pipeline.project_id
  account_id   = "hello-app-deployer"
  display_name = "hello-app-deployer"
  description  = "Service Account for creating Cloud Deploy Releases"
}

# hello-app-deployer Service Account needs permissions to upload artifacts.json to the bucket.
resource "google_storage_bucket_iam_member" "hello-app-deployer_objectCreator" {
  bucket = google_storage_bucket.storage.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.hello-app-deployer.email}"
}

resource "google_storage_bucket_iam_member" "hello-app-deployer_legacyBucketsReader" {
  bucket = google_storage_bucket.storage.name
  role   = "roles/storage.legacyBucketReader"
  member = "serviceAccount:${google_service_account.hello-app-deployer.email}"
}

# hello-app-deployer Service Account needs permissions to push images to Artifact Registry.
resource "google_artifact_registry_repository_iam_member" "hello-app-deployer" {
  project    = google_artifact_registry_repository.hello-app.project
  location   = google_artifact_registry_repository.hello-app.location
  repository = google_artifact_registry_repository.hello-app.name
  role       = "roles/artifactregistry.writer"
  member     = "serviceAccount:${google_service_account.hello-app-deployer.email}"
}

# hello-app-deployer Service Account needs permissions to act as the Service Account for the Cloud Deploy Target.
resource "google_service_account_iam_member" "deployer-as-hello-app-target" {
  for_each = local.projects

  service_account_id = google_service_account.hello-app-target[each.key].name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.hello-app-deployer.email}"
}

// -------- hello-app-stg-promoter Service Account -------- //

resource "google_service_account" "hello-app-stg-promoter" {
  project      = google_project.pipeline.project_id
  account_id   = "hello-app-stg-promoter"
  display_name = "hello-app-stg-promoter"
  description  = "Service Account for promoting hello-app to stg"
}

resource "google_service_account_iam_member" "hello-app-stg-promoter-as-hello-app-target" {
  service_account_id = google_service_account.hello-app-target["stg"].name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.hello-app-stg-promoter.email}"
}

// -------- hello-app-prd-promoter Service Account -------- //

resource "google_service_account" "hello-app-prd-promoter" {
  project      = google_project.pipeline.project_id
  account_id   = "hello-app-prd-promoter"
  display_name = "hello-app-prd-promoter"
  description  = "Service Account for promoting hello-app to prd"
}

resource "google_service_account_iam_member" "hello-app-prd-promoter-as-hello-app-target" {
  service_account_id = google_service_account.hello-app-target["prd"].name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.hello-app-prd-promoter.email}"
}

// -------- Cloud Storage Bucket for source and rendered manifests -------- //

resource "google_storage_bucket" "storage" {
  project                     = google_project.pipeline.project_id
  location                    = var.region
  name                        = google_project.pipeline.project_id
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 7
    }
  }
}

// -------- Artifact Registry -------- //
resource "google_artifact_registry_repository" "hello-app" {
  project       = google_project.pipeline.project_id
  location      = var.region
  repository_id = "hello-app"
  format        = "DOCKER"

  depends_on = [google_project_service.artifactregistry]
}

resource "google_artifact_registry_repository_iam_member" "service-agent" {
  for_each = local.projects

  project    = google_artifact_registry_repository.hello-app.project
  location   = google_artifact_registry_repository.hello-app.location
  repository = google_artifact_registry_repository.hello-app.name
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:service-${google_project.service[each.key].number}@serverless-robot-prod.iam.gserviceaccount.com"
}

// -------- Cloud Deploy Target -------- //

resource "google_service_account" "hello-app-target" {
  for_each = local.projects

  project      = google_project.pipeline.project_id
  account_id   = "hello-app-target-${each.key}"
  display_name = "hello-app-target-${each.key}"
  description  = "Service Account for Cloud Deploy Target in ${each.key} environment"
}

# hello-app-target Service Account needs permissions to write logs.
resource "google_project_iam_member" "hello-app-target_logging_logWriter" {
  for_each = local.projects

  project = google_project.pipeline.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.hello-app-target[each.key].email}"
}

# hello-app-target SA needs permissions to get sources from Cloud Storage.
resource "google_storage_bucket_iam_member" "hello-app-target_storage_objectViewer" {
  for_each = local.projects

  bucket = google_storage_bucket.storage.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.hello-app-target[each.key].email}"
}

# hello-app-target SA needs permissions to upload artifacts to Cloud Storage.
resource "google_storage_bucket_iam_member" "hello-app-target_storage_objectCreator" {
  for_each = local.projects

  bucket = google_storage_bucket.storage.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.hello-app-target[each.key].email}"
}

# hello-app-target Service Account needs permissions to act as the Service Account for the Cloud Run Service.
resource "google_service_account_iam_member" "hello-app-target-as-hello-app" {
  for_each = local.projects

  service_account_id = google_service_account.hello-app[each.key].name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.hello-app-target[each.key].email}"
}

# hello-app-target Service Account needs permissions to deploy to Cloud Run.
resource "google_cloud_run_v2_service_iam_member" "hello-app-target_run_developer" {
  for_each = local.projects

  project  = google_cloud_run_v2_service.hello-app[each.key].project
  location = google_cloud_run_v2_service.hello-app[each.key].location
  name     = google_cloud_run_v2_service.hello-app[each.key].name
  role     = "roles/run.developer"
  member   = "serviceAccount:${google_service_account.hello-app-target[each.key].email}"
}

resource "google_clouddeploy_target" "hello-app" {
  for_each = local.projects

  project          = google_project.pipeline.project_id
  location         = var.region
  name             = "hello-app-${each.key}"
  require_approval = false

  execution_configs {
    usages           = ["RENDER", "DEPLOY"]
    service_account  = google_service_account.hello-app-target[each.key].email
    artifact_storage = "gs://${google_storage_bucket.storage.name}/artifacts"
  }

  run {
    location = "projects/${each.value}/locations/${var.region}"
  }

  deploy_parameters = {
    message              = "Hello, ${each.key}!"
    service_account_name = google_service_account.hello-app[each.key].email
  }

  depends_on = [google_project_service.clouddeploy]
}

// -------- Cloud Deploy Delivery Pipeline -------- //
resource "google_clouddeploy_delivery_pipeline" "hello-app" {
  project     = google_project.pipeline.project_id
  location    = var.region
  name        = "hello-app"
  description = "Delivery Pipeline for hello-app"

  serial_pipeline {
    stages {
      target_id = google_clouddeploy_target.hello-app["dev"].name
    }

    stages {
      target_id = google_clouddeploy_target.hello-app["stg"].name
    }

    stages {
      target_id = google_clouddeploy_target.hello-app["prd"].name
    }
  }
}

resource "google_project_iam_custom_role" "clouddeploy_releaser" {
  project     = google_project.pipeline.project_id
  role_id     = "clouddeployReleaseCreator"
  title       = "Cloud Deploy Release Creator"
  description = "Custom role to create releases in Cloud Deploy"
  permissions = ["clouddeploy.releases.create"]
}

data "google_iam_policy" "hello-app" {
  binding {
    role    = google_project_iam_custom_role.clouddeploy_releaser.id
    members = ["serviceAccount:${google_service_account.hello-app-deployer.email}"]
  }

  binding {
    role    = "roles/clouddeploy.releaser"
    members = ["serviceAccount:${google_service_account.hello-app-deployer.email}"]
    condition {
      title      = "Rollout to hello-app-dev"
      expression = "api.getAttribute(\"clouddeploy.googleapis.com/rolloutTarget\", \"\") == \"${google_clouddeploy_target.hello-app["dev"].name}\""
    }
  }

  binding {
    role    = "roles/clouddeploy.releaser"
    members = ["serviceAccount:${google_service_account.hello-app-stg-promoter.email}"]
    condition {
      title      = "Rollout to hello-app-stg"
      expression = "api.getAttribute(\"clouddeploy.googleapis.com/rolloutTarget\", \"\") == \"${google_clouddeploy_target.hello-app["stg"].name}\""
    }
  }

  binding {
    role    = "roles/clouddeploy.releaser"
    members = ["serviceAccount:${google_service_account.hello-app-prd-promoter.email}"]
    condition {
      title      = "Rollout to hello-app-prd"
      expression = "api.getAttribute(\"clouddeploy.googleapis.com/rolloutTarget\", \"\") == \"${google_clouddeploy_target.hello-app["prd"].name}\""
    }
  }
}

resource "google_clouddeploy_delivery_pipeline_iam_policy" "policy" {
  project     = google_clouddeploy_delivery_pipeline.hello-app.project
  location    = google_clouddeploy_delivery_pipeline.hello-app.location
  name        = google_clouddeploy_delivery_pipeline.hello-app.name
  policy_data = data.google_iam_policy.hello-app.policy_data
}

// -------- Permissions for Cloud Deploy Rollout creators -------- //

locals {
  rollout_creators = {
    deployer     = "serviceAccount:${google_service_account.hello-app-deployer.email}",
    stg_promoter = "serviceAccount:${google_service_account.hello-app-stg-promoter.email}",
    prd_promoter = "serviceAccount:${google_service_account.hello-app-prd-promoter.email}",
  }
}

resource "google_project_iam_member" "hello-app-deployer_clouddeploy_viewer" {
  for_each = local.rollout_creators

  project = google_project.pipeline.project_id
  role    = "roles/clouddeploy.viewer"
  member  = each.value
}