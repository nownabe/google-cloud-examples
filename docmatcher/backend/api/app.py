from fastapi import FastAPI
from google.cloud.spanner_v1.database import Database

from .v1.app import create_app as create_v1
from .v1.document_event_publisher import DocumentEventPublisher


V1_ROOT_PATH = "/api/v1"


def create_app(spanner_db: Database,
               document_event_publisher: DocumentEventPublisher) -> FastAPI:
    app = FastAPI()

    v1 = create_v1(root_path=V1_ROOT_PATH,
                   spanner_db=spanner_db,
                   document_event_publisher=document_event_publisher)

    app.mount(V1_ROOT_PATH, v1)

    return app
