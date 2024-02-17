locals {
  envs = ["dev", "stg", "prd"]
}

resource "google_project" "service" {
  for_each = { for env in local.envs : env => "${var.project_prefix}-${env}" }

  name            = "${var.project_prefix}-${each.key}"
  project_id      = "${var.project_prefix}-${each.key}"
  billing_account = data.google_billing_account.billing.id
}

locals {
  projects = { for env in local.envs : env => google_project.service[env].project_id }
}

resource "google_project_service" "run" {
  for_each = local.projects

  project = each.value
  service = "run.googleapis.com"
}

resource "google_service_account" "hello-app" {
  for_each = local.projects

  project      = each.value
  account_id   = "hello-app"
  display_name = "hello-app"
  description  = "Service Account for app in ${each.key} environment"
}

resource "google_cloud_run_v2_service" "hello-app" {
  for_each = local.projects

  project  = each.value
  location = var.region
  name     = "hello-app"

  template {
    service_account = google_service_account.hello-app[each.key].email
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello:latest"
    }
  }

  ingress = "INGRESS_TRAFFIC_ALL"

  depends_on = [google_project_service.run]
  lifecycle {
    ignore_changes = [template]
  }
}

resource "google_cloud_run_v2_service_iam_member" "allow_unauthenticated" {
  for_each = local.projects

  project  = google_cloud_run_v2_service.hello-app[each.key].project
  location = google_cloud_run_v2_service.hello-app[each.key].location
  name     = google_cloud_run_v2_service.hello-app[each.key].name
  role     = "roles/run.invoker"
  member   = "allUsers"
}