from fastapi import FastAPI, status
from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str = Field(description="Document ID")
    content: str = Field(description="Content")


class SearchDocumentsResponse(BaseModel):
    """Response for /api/v1/documents:search"""
    documents: list[Document]


class Evaluation(BaseModel):
    text: str = Field(description="Text to search")
    document_id: str = Field(description="Searched document ID")
    score: float = Field(description="Score on a search result")


def create_app(root_path: str) -> FastAPI:
    app = FastAPI(root_path=root_path)

    @app.post("/documents", response_model=Document)
    async def create_document(document: Document):
        return document

    @app.get("/documents:search", response_model=SearchDocumentsResponse)
    async def search_documents():
        doc1 = Document(id="doc1", content="Lorem Ipsum"*100)
        doc2 = Document(id="doc2", content="Lorem Ipsum"*100)

        response = SearchDocumentsResponse(documents=[doc1, doc2])

        return response

    @app.post("/evaluations", status_code=status.HTTP_204_NO_CONTENT)
    async def create_evaluation(evaluation: Evaluation):
        return None

    return app
