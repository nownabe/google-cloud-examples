from os import environ

import grpc
from google.cloud import spanner

from api.app import create_app
from gen.docmatcher.vectorizer_pb2_grpc import VectorizerServiceStub


spanner_db = spanner.Client(project=environ["SPANNER_PROJECT_ID"]) \
                    .instance(environ["SPANNER_INSTANCE_ID"]) \
                    .database(environ["SPANNER_DATABASE_ID"])

vectorizer = VectorizerServiceStub(grpc.insecure_channel("localhost:3003"))

app = create_app(spanner_db=spanner_db, vectorizer=vectorizer)


if __name__ == "__main__":
    import uvicorn

    port = int(environ.get("PORT", "3001"))
    log_level = environ.get("LOG_LEVEL", "info")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level=log_level)
