from pydantic import BaseModel, Field
from typing import Optional



class Chunk(BaseModel):
    """A fragment of text within a page."""
    id: str
    text: str
    metadata: Optional[dict] = Field(default_factory=dict)



