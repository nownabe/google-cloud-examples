from os import environ

from google.cloud import spanner

from api.app import create_app
from api.document_event_publisher import DocumentEventPublisher


spanner_db = spanner.Client(project=environ["SPANNER_PROJECT_ID"]) \
                    .instance(environ["SPANNER_INSTANCE_ID"]) \
                    .database(environ["SPANNER_DATABASE_ID"])

doc_event_publisher = DocumentEventPublisher(environ["PUBSUB_PROJECT_ID"],
                                             environ["PUBSUB_TOPIC_ID"])

app = create_app(spanner_db=spanner_db,
                 document_event_publisher=doc_event_publisher)


if __name__ == "__main__":
    import uvicorn

    port = int(environ.get("PORT", "3001"))
    log_level = environ.get("LOG_LEVEL", "info")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level=log_level)
