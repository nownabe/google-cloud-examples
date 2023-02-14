resource "google_pubsub_schema" "document-event" {
  name       = "document-event"
  type       = "PROTOCOL_BUFFER"
  definition = file("../backend/proto/docmatcher/v1/document_event.proto")
}

resource "google_pubsub_topic" "document-events" {
  name = "document-events"
  schema_settings {
    schema   = google_pubsub_schema.document-event.id
    encoding = "JSON"
  }
}
