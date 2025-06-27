import io
import pprint

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from PIL import Image
from pydantic import BaseModel

from rag.domain.base_vector_store import VectorStoreRepository
from rag.services.document_loading_service import DocumentService
from rag.services.image_loader import ImageLoader
from rag.services.ocr_pipeline import preprocess_image, run_easyocr_on_image
from rag.services.pdf_loader import PdfLoader
from rag.services.standard_preprocess import StandardImagePreprocess
from rag.services.weaviate_retrieval_provider import WeaviateRetrievalProvider
from rag.web.api.extract_entities.schema import DocumentRequest, FileExtension

router = APIRouter()


class Item(BaseModel):
    title: str
    description: str


@router.post("/")
async def send_echo_message(

    repository: VectorStoreRepository = Depends(WeaviateRetrievalProvider),

) -> list[dict]:

    """
    Sends extract_entities back to user.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """

    return temp


@router.post("/hola")
async def send_echo_message(
    data: list[dict],
    repository: VectorStoreRepository = Depends(WeaviateRetrievalProvider),
) -> str:
    temp = await repository.add_documents(data)

    return temp



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
    file: UploadFile = File(...),
    vector_store: VectorStoreRepository = Depends(WeaviateRetrievalProvider)
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

        case _:
            return DocumentService(document_loader=PdfLoader(), vector_store=vector_store)




@router.post("")
async def upload_file(
    document_request: DocumentRequest = Depends(validate_upload),
    document_service: DocumentService = Depends(select_loader),

) -> list[dict]:
    # Check file extension

    # Read file content into memory

    result = await document_service.add_document(document_request.content)

    return result
