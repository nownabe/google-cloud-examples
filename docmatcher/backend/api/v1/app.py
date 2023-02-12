from fastapi import FastAPI, status
from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str = Field(description="Document ID")
    content: str = Field(description="Content")


class CreateDocumentRequest(BaseModel):
    content: str = Field(description="Content")


class SearchDocumentsResponse(BaseModel):
    documents: list[Document]


class Feedback(BaseModel):
    content: str = Field(description="Content to search")
    document_id: str = Field(description="Searched document ID")
    score: float = Field(description="Score on a search result")


def create_app(root_path: str) -> FastAPI:
    app = FastAPI(root_path=root_path)

    @app.post("/documents", response_model=Document)
    async def create_document(req: CreateDocumentRequest):
        return Document(id="docid", content=req.content)

    @app.get("/documents:search", response_model=SearchDocumentsResponse)
    async def search_documents(content: str):
        doc1 = Document(id="doc1", content=content*10)
        doc2 = Document(id="doc2", content=content*10)

        response = SearchDocumentsResponse(documents=[doc1, doc2])

        return response

    @app.post("/feedbacks", status_code=status.HTTP_204_NO_CONTENT)
    async def create_feedback(feedback: Feedback):
        return None

    return app
