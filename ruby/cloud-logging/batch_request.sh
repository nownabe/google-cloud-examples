#/usr/bin/env bash

url="$1"

curl -w "\n" "${url}/set_project"
curl -w "\n" "${url}/text_payload"
curl -w "\n" "${url}/json_payload"
curl -w "\n" "${url}/message"
curl -w "\n" "${url}/severity"
curl -w "\n" "${url}/time"
curl -w "\n" "${url}/source_location"
curl -w "\n" "${url}/trace"
curl -w "\n" "${url}/stack_trace"
curl -w "\n" "${url}/labels"
curl -w "\n" "${url}/insert_id"
curl -w "\n" "${url}/http_request"
curl -w "\n" "${url}/operation"