from pydantic import BaseModel, Field
from typing import List, Optional

from rag.domain.models.chunk import Chunk


class Page(BaseModel):
    """A single page of a document."""
    number: int
    content: list[str]
    chunks: List[Chunk] = Field(default_factory=list)
    metadata: Optional[dict] = Field(default_factory=dict)
    raw_content: bytes
