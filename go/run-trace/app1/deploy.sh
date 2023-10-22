#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

tag="$(date +%Y%m%d%H%M%S)"

app2url="$(gcloud run services describe run-trace-2 --region us-central1 --format 'value(status.url)')"

docker build -t "us-central1-docker.pkg.dev/${PROJECT_ID}/google-cloud-examples/go/run-trace:${tag}" .
docker push "us-central1-docker.pkg.dev/${PROJECT_ID}/google-cloud-examples/go/run-trace:${tag}"
gcloud run deploy run-trace \
  --project "${PROJECT_ID}" \
  --region us-central1 \
  --image "us-central1-docker.pkg.dev/${PROJECT_ID}/google-cloud-examples/go/run-trace:${tag}" \
  --allow-unauthenticated \
  --set-env-vars "APP2_URL=${app2url}"