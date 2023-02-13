from uuid import uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from google.cloud.spanner_v1.database import Database

from .models import Document, Feedback
from .document_event_publisher import DocumentEventPublisher


class CreateDocumentRequest(BaseModel):
    content: str = Field(description="Content")


class SearchDocumentsResponse(BaseModel):
    documents: list[Document] = Field(description="Searched similar documents")


def create_app(root_path: str,
               spanner_db: Database,
               document_event_publisher: DocumentEventPublisher) -> FastAPI:
    app = FastAPI(root_path=root_path)

    @app.post("/documents", response_model=Document)
    async def create_document(req: CreateDocumentRequest):
        doc = Document(id=str(uuid4()), content=req.content)

        with spanner_db.batch() as batch:
            batch.insert(
                table="Documents",
                columns=("DocumentId", "Content"),
                values=[(doc.id, doc.content)]
            )

        document_event_publisher.publish(doc)

        return doc

    @app.get("/documents:search", response_model=SearchDocumentsResponse)
    async def search_documents(content: str):
        # search
        doc1 = Document(id="doc1", content=f"{content} "*20)
        doc2 = Document(id="doc2", content=f"{content[::-1]} "*20)

        response = SearchDocumentsResponse(documents=[doc1, doc2])

        return response

    @app.post("/feedbacks", status_code=status.HTTP_204_NO_CONTENT)
    async def create_feedback(feedback: Feedback):
        # publish feedback event
        return None

    return app
