#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

tag="$(date +%Y%m%d%H%M%S)"

docker build -t "us-central1-docker.pkg.dev/${PROJECT_ID}/google-cloud-examples/go/run-trace-2:${tag}" .
docker push "us-central1-docker.pkg.dev/${PROJECT_ID}/google-cloud-examples/go/run-trace-2:${tag}"
gcloud run deploy run-trace-2 \
  --project "${PROJECT_ID}" \
  --region us-central1 \
  --image "us-central1-docker.pkg.dev/${PROJECT_ID}/google-cloud-examples/go/run-trace-2:${tag}" \
  --allow-unauthenticated