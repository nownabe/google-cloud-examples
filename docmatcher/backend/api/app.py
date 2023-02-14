from uuid import uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from google.cloud.spanner_v1.database import Database

from .models import Document, Feedback
from gen.docmatcher.vectorizer_pb2 import VectorizeRequest
from gen.docmatcher.vectorizer_pb2_grpc import VectorizerServiceStub


class CreateDocumentRequest(BaseModel):
    content: str = Field(description="Content")


class SearchDocumentsResponse(BaseModel):
    documents: list[Document] = Field(description="Searched similar documents")


def create_app(spanner_db: Database,
               vectorizer: VectorizerServiceStub) -> FastAPI:
    app = FastAPI()

    @app.post("/api/documents", response_model=Document)
    async def create_document(req: CreateDocumentRequest):
        doc = Document(id=str(uuid4()), content=req.content)

        with spanner_db.batch() as batch:
            batch.insert(
                table="Documents",
                columns=("DocumentId", "Content"),
                values=[(doc.id, doc.content)]
            )

        response = vectorizer.Vectorize(VectorizeRequest(content=doc.content))
        vector = response.vector
        print(vector)  # TODO: delete

        return doc

    @app.get("/api/documents:search", response_model=SearchDocumentsResponse)
    async def search_documents(content: str):
        # search
        doc1 = Document(id="doc1", content=f"{content} "*20)
        doc2 = Document(id="doc2", content=f"{content[::-1]} "*20)

        response = SearchDocumentsResponse(documents=[doc1, doc2])

        return response

    @app.post("/api/feedbacks", status_code=status.HTTP_204_NO_CONTENT)
    async def create_feedback(feedback: Feedback):
        # publish feedback event
        return None

    return app
