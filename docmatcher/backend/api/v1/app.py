from uuid import uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from google.cloud.spanner_v1.database import Database


class Document(BaseModel):
    id: str = Field(description="Document ID")
    content: str = Field(description="Content")


class CreateDocumentRequest(BaseModel):
    content: str = Field(description="Content")


class SearchDocumentsResponse(BaseModel):
    documents: list[Document] = Field(description="Searched similar documents")


class Feedback(BaseModel):
    content: str = Field(description="Content to search")
    document_id: str = Field(description="Searched document ID")
    score: float = Field(description="Score on a search result")


def create_app(root_path: str, spanner_db: Database) -> FastAPI:
    app = FastAPI(root_path=root_path)

    @app.post("/documents", response_model=Document)
    async def create_document(req: CreateDocumentRequest):
        document_id = str(uuid4())

        with spanner_db.batch() as batch:
            batch.insert(
                table="Documents",
                columns=("DocumentId", "Content"),
                values=[(document_id, req.content)]
            )

        # publish insert event

        return Document(id=document_id, content=req.content)

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
