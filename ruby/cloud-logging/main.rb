require "json"
require "net/http"
require "securerandom"
require "time"

require "sinatra"
require "sinatra/reloader" if development?

set :logging, false
set :port, ENV["PORT"] || 8080

$project = "local-project"

def set_project
  begin
    Net::HTTP.new("metadata.google.internal").start do |http|
      response = http.get("/computeMetadata/v1/project/project-id", "Metadata-Flavor" => "Google")
      $project = response.body
    end
  rescue => e
    pp e
  end
end

def emit(log)
  log = log.to_json if log.is_a?(Hash)
  $stderr.puts log
  log
end

get "/" do
  "ok"
end

get "/set_project" do
  set_project
  "project #{$project}"
end

get "/text_payload" do
  log = "Hello, Cloud Logging!"
  emit(log)
end

get "/json_payload" do
  log = {
    text: "Hello, Cloud Logging!",
    key1: "value1",
    key2: "value2",
  }
  emit(log)
end

get "/message" do
  log = {
    message: "Hello, Cloud Logging!",
    key1: "value1",
    key2: "value2",
  }
  emit(log)
end

get "/severity/:severity" do
  severity = params["severity"] || "INFO"
  log = {
    message: "Hello, Cloud Logging! severity=#{severity}",
    severity: severity,
    key1: "value1",
  }
  emit(log)
end

get "/time" do
  t = Time.now + 30 * 60 # 30 minutes later
  log = {
    message: "Hello, Cloud Logging! with time",
    severity: "INFO",
    time: Time.new(t.year, t.month, t.day, t.hour, t.min, t.sec).utc.iso8601(9), # nano seconds
    key1: "value1",
  }
  emit(log)
end

def some_func
  Thread.current.backtrace[1].split(":")
end

get "/source_location" do
  file, line, function = some_func
  log = {
    message: "Hello, Cloud Logging! with sourceLocation",
    severity: "INFO",
    key1: "value1",
    "logging.googleapis.com/sourceLocation": {
      file: file,
      line: line,
      function: function,
    }
  }
  emit(log)
end

get "/trace" do
  trace_id, span_id = request.env["HTTP_X_CLOUD_TRACE_CONTEXT"].split(";")[0].split("/")
  log = {
    message: "Hello, Cloud Logging! with trace",
    severity: "INFO",
    key1: "value1",
    "logging.googleapis.com/trace": "projects/#{$project}/traces/#{trace_id}",
    "logging.googleapis.com/spanId": span_id,
    "logging.googleapis.com/trace_sampled": true,
  }
  emit(log)
end

def some_error_func
  raise "some error"
end

get "/stack_trace" do
  begin
    some_error_func
  rescue => e
    log = {
      message: e.message,
      severity: "ERROR",
      key1: "value1",
      stack_trace: e.message + "\n" + e.backtrace.join("\n"),
    }
    emit(log)
  end
end

# Useful

get "/labels" do
  log = {
    message: "Hello, Cloud Logging! with labels",
    severity: "INFO",
    key1: "value1",
    "logging.googleapis.com/labels": {
      label1: "value1",
      label2: "value2",
    },
  }
  emit(log)
end

# Optional

get "/insert_id" do
  log = {
    message: "Hello, Cloud Logging! with insertId",
    severity: "INFO",
    key1: "value1",
    "logging.googleapis.com/insertId": SecureRandom.uuid,
  }
  emit(log)
end

get "/http_request" do
  log = {
    message: "Hello, Cloud Logging! with httpRequest",
    severity: "INFO",
    key1: "value1",
    httpRequest: {
      requestMethod: request.request_method,
      requestUrl: request.url,
      requestSize: "123",
      status: 200,
      responseSize: "456",
      userAgent: request.user_agent,
      remoteIp: request.ip,
      serverIp: "172.0.0.1",
      referer: request.referer,
      latency: "3.5s",
      cacheLookup: false,
      cacheHit: false,
      cacheValidatedWithOriginServer: false,
      cacheFillBytes: "0",
      protocol: "HTTP/1.1",
    },
  }
  emit(log)
end

get "/operation" do
  producer = "cloud-logging-example"
  operation_id = "operation/#{SecureRandom.uuid}"

  log = {
    message: "/operation started",
    severity: "INFO",
    key1: "value1",
    "logging.googleapis.com/operation": {
      id: operation_id,
      producer: producer,
      first: true,
      last: false,
    },
  }
  emit(log)

  log = {
    message: "/operation is running",
    severity: "INFO",
    key1: "value1",
    "logging.googleapis.com/operation": {
      id: operation_id,
      producer: producer,
      first: false,
      last: false,
    },
  }
  emit(log)

  log = {
    message: "/operation finished",
    severity: "INFO",
    key1: "value1",
    "logging.googleapis.com/operation": {
      id: operation_id,
      producer: producer,
      first: false,
      last: true,
    },
  }
  emit(log)
end