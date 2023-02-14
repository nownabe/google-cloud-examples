from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str = Field(description="Document ID")
    content: str = Field(description="Content")


class Feedback(BaseModel):
    content: str = Field(description="Content to search")
    document_id: str = Field(description="Searched document ID")
    score: float = Field(description="Score on a search result")
