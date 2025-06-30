import functools

from PIL import UnidentifiedImageError
from fastapi import HTTPException, UploadFile, File
from fastapi.params import Depends

from rag.domain.base_vector_store import VectorStoreRepository
from rag.services.document_loading_service import DocumentService
from rag.services.image_loader import ImageLoader
from rag.services.pdf_loader import PdfLoader
from rag.services.document_weaviate_repository import DocumentWeaviateRepository

from rag.web.api.extract_entities.schema import DocumentRequest, FileExtension


async def validate_upload(file: UploadFile = File(...)) -> DocumentRequest:
    allowed_exts = {".png", ".jpg", ".jpeg", ".pdf"}
    allowed_mimes = {"image/png", "image/jpeg", "application/pdf"}

    filename = file.filename.lower()
    ext_valid = ""
    for ext in allowed_exts:
        if filename.endswith(ext):
            ext_valid = ext
            break

    mime_valid = file.content_type in allowed_mimes

    if not (ext_valid and mime_valid):
        raise HTTPException(status_code=400, detail="Invalid file type")

    content = await file.read()
    return DocumentRequest(content=content, file_type=FileExtension(ext_valid))


def select_loader(
    file: UploadFile | None = File(...),
    vector_store: VectorStoreRepository = Depends(DocumentWeaviateRepository)
) -> DocumentService:
    filename = file.filename.lower()
    allowed_extensions = {".png", ".jpg", ".jpeg", ".pdf"}
    extension = next((ext for ext in allowed_extensions if filename.endswith(ext)), None)

    match FileExtension(extension):

        case FileExtension.JPG | FileExtension.JPEG | FileExtension.PNG:
            return DocumentService(
                document_loader=ImageLoader(),
                vector_store=vector_store
            )

        case FileExtension.PDF:
            return DocumentService(document_loader=PdfLoader(), vector_store=vector_store)

        case _:
            return DocumentService(document_loader=PdfLoader(), vector_store=vector_store)



def document_service_creator(vector_store: VectorStoreRepository = Depends(DocumentWeaviateRepository)):
    return DocumentService(document_loader=PdfLoader(), vector_store=vector_store)
