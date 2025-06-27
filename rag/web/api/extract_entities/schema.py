from pydantic import BaseModel


from enum import StrEnum

class FileExtension(StrEnum):
    PNG = ".png"
    JPG = ".jpg"
    JPEG = ".jpeg"
    PDF = ".pdf"

class DocumentRequest(BaseModel):
    """Simple message model."""

    content: bytes
    file_type: FileExtension
