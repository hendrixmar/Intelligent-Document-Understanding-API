import io
import pprint

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from PIL import Image
from pydantic import BaseModel

from rag.domain.base_vector_store import VectorStoreRepository
from rag.services.ocr_pipeline import preprocess_image, run_easyocr_on_image
from rag.services.weaviate_retrieval_provider import WeaviateRetrievalProvider
from rag.web.api.extract_entities.schema import Message, DocumentRequest, FileExtension

router = APIRouter()


class Item(BaseModel):
    title: str
    description: str


@router.post("/")
async def send_echo_message(
    incoming_message: Message,
    repository: VectorStoreRepository = Depends(WeaviateRetrievalProvider),
) -> list[dict]:
    temp = await repository.similarity_search(incoming_message.message)
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

@router.post("")
async def upload_file(file: DocumentRequest =  Depends(validate_upload)):
    # Check file extension

    # Read file content into memory

    pprint.pprint(
        file
    )
