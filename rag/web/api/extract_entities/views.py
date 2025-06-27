import io

from fastapi import APIRouter, File, UploadFile
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from PIL import Image
from pydantic import BaseModel

from rag.domain.base_vector_store import VectorStoreRepository
from rag.services.ocr_pipeline import preprocess_image, run_easyocr_on_image
from rag.services.weaviate_retrieval_provider import WeaviateRetrievalProvider
from rag.web.api.extract_entities.schema import Message

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


@router.post("")
async def upload_file(file: UploadFile = File(...)):
    # Check file extension
    allowed_extensions = {".jpg", ".jpeg", ".png", ".pdf"}
    filename = file.filename
    extension = filename[filename.rfind(".") :].lower()

    if extension not in allowed_extensions:
        return JSONResponse(content={"error": "Invalid file type"}, status_code=400)

    # Read file content into memory
    contents = await file.read()
    image_stream = io.BytesIO(contents)

    # Open it as a PIL image
    image = Image.open(image_stream)

    preprocessed_image = preprocess_image(image)
    results = run_easyocr_on_image(preprocessed_image)
    # --------- Corregir texto ----


    # Now 'contents' is a bytes object containing the file data
    # You can process it, e.g. save to DB, analyze, etc.
    file_size_kb = len(contents) / 1024

    # return {
    #     "filename": filename,
    #     "content_type": file.content_type,
    #     "size_kb": f"{file_size_kb:.2f}",
    #     "results": results
    # }
    return [e for e in many_chunks]
