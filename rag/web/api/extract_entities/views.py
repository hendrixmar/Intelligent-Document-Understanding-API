from fastapi import APIRouter
from fastapi.params import Depends

from rag.services.document_loading_service import DocumentService
from rag.utils import document_service_creator

router = APIRouter()





@router.get("")
async def similarity_search(
    query: str,
    k: int = 20,
    document_service: DocumentService = Depends(document_service_creator),
) -> list[dict]:
    # Check file extension

    # Read file content into memory

    result = await document_service.search_document(query, k)

    return result
