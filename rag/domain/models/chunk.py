from uuid import uuid4, UUID

from pydantic import BaseModel, Field
from typing import Optional



class Chunk(BaseModel):
    """A fragment of text within a page."""
    id:  UUID = Field(default_factory=uuid4)
    text: str
    metadata: Optional[dict] = Field(default_factory=dict)



