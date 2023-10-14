#/usr/bin/env bash

url="$1"

curl -w "\n" "${url}/set_project"
curl -w "\n" "${url}/text_payload"
curl -w "\n" "${url}/json_payload"
curl -w "\n" "${url}/message"
curl -w "\n" "${url}/severity/DEFAULT"
curl -w "\n" "${url}/severity/DEBUG"
curl -w "\n" "${url}/severity/INFO"
curl -w "\n" "${url}/severity/NOTICE"
curl -w "\n" "${url}/severity/WARNING"
curl -w "\n" "${url}/severity/ERROR"
curl -w "\n" "${url}/severity/CRITICAL"
curl -w "\n" "${url}/severity/ALERT"
curl -w "\n" "${url}/severity/EMERGENCY"
curl -w "\n" "${url}/time"
curl -w "\n" "${url}/source_location"
curl -w "\n" "${url}/trace"
curl -w "\n" "${url}/stack_trace"
curl -w "\n" "${url}/labels"
curl -w "\n" "${url}/insert_id"
curl -w "\n" "${url}/http_request"
curl -w "\n" "${url}/operation"