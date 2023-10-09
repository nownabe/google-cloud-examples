#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

tag="$(date +%Y%m%d%H%M%S)"

docker build -t "us-central1-docker.pkg.dev/${PROJECT_ID}/google-cloud-examples/ruby/cloud-logging:${tag}" .
docker push "us-central1-docker.pkg.dev/${PROJECT_ID}/google-cloud-examples/ruby/cloud-logging:${tag}"
gcloud run deploy cloud-logging \
  --project "${PROJECT_ID}" \
  --region us-central1 \
  --image "us-central1-docker.pkg.dev/${PROJECT_ID}/google-cloud-examples/ruby/cloud-logging:${tag}" \
  --allow-unauthenticated