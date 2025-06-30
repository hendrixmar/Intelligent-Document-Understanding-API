from typing import List
from pydantic import BaseModel, Field, validator, field_validator
from typing import Optional
from datetime import datetime
from rag.domain.models.page import Page
from uuid import uuid4, UUID


from enum import StrEnum


class DocumentCategory(StrEnum):
    ADVERTISEMENT = "advertisement"
    BUDGET = "budget"
    EMAIL = "email"
    FILE_FOLDER = "file_folder"
    FORM = "form"
    HANDWRITTEN = "handwritten"
    INVOICE = "invoice"
    LETTER = "letter"
    MEMO = "memo"
    NEWS_ARTICLE = "news_article"
    PRESENTATION = "presentation"
    QUESTIONNAIRE = "questionnaire"
    RESUME = "resume"
    SCIENTIFIC_PUBLICATION = "scientific_publication"
    SCIENTIFIC_REPORT = "scientific_report"
    SPECIFICATION = "specification"

class DocumentMetadata(BaseModel):
    """Metadata associated with a document or file."""
    creation_date: datetime = Field(default_factory=datetime.now,
                                    description="Date and time the document was created.")
    file_type: str = Field(...,
                           description="Type or format of the document (e.g., pdf, jpeg).")
    file_size: int = Field(..., description="Size of the file in bytes.")

    author: Optional[str] = Field(None, description="Name of the document's author.")
    source: Optional[str] = Field(None,
                                  description="Source of the document (e.g., upload, scanner, URL).")
    language: Optional[str] = Field(None,
                                    description="Language of the document content (e.g., en, es).")

    @field_validator("creation_date", mode="before")
    @classmethod
    def set_creation_date_now(cls, v):
        return v or datetime.now()

class Document(BaseModel):
    """A document composed of multiple pages."""
    id: UUID = Field(default_factory=uuid4)
    title: Optional[str] = None
    category: DocumentCategory | None = None
    pages: List[Page] = Field(default_factory=list)
    metadata: Optional[DocumentMetadata] = Field()
