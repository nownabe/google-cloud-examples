from base64 import b64decode
from logging import getLogger
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from google.protobuf.json_format import Parse

from gen.docmatcher.v1 import document_event_pb2 as pb
from .vectorizer import Vectorizer


logger = getLogger("uvicorn")


class PubSubMessage(BaseModel):
    attributes: Optional[dict[str, str]]
    data: str
    message_id: str
    messageId: str
    publish_time: str
    publishTime: str


class PubSubEnvelope(BaseModel):
    """
    Request body from Pub/Sub push subscription
    See https://cloud.google.com/pubsub/docs/push#receive_push
    """

    message: PubSubMessage
    subscription: str


class Response(BaseModel):
    ok: bool


def create_app(vectorizer: Vectorizer) -> FastAPI:
    app = FastAPI()

    @app.get("/", response_model=Response)
    async def root():
        return Response(ok=True)

    @app.post("/", response_model=Response)
    async def update_vector(envelope: PubSubEnvelope):
        message = envelope.message
        logger.info("received message: id=%s", message.message_id)

        data = b64decode(message.data)
        print(str(data))

        doc_event = pb.DocumentEvent()
        Parse(data, doc_event)
        print(doc_event)
        vector = vectorizer.vectorize(doc_event.content)
        print(vector)

        return Response(ok=True)

    return app
