from google.cloud.pubsub_v1.publisher import Client
from google.protobuf.json_format import MessageToJson

from gen.docmatcher import document_event_pb2 as pb
from .models import Document


class DocumentEventPublisher:
    def __init__(self, project_id: str, topic_id: str):
        self._client = Client()
        self._topic_path = self._client.topic_path(project_id, topic_id)
        print(self._client)
        print(self._topic_path)

    def publish(self, document: Document) -> None:
        event = pb.DocumentEvent()
        event.document_id = document.id
        event.content = document.content

        data = str(MessageToJson(event)).encode("utf-8")
        self._client.publish(self._topic_path, data).result()
