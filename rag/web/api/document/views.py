from fastapi import APIRouter, Depends

from rag.domain.models.document import Document
from rag.services.document_loading_service import DocumentService
from rag.utils import validate_upload, select_loader
from rag.web.api.extract_entities.schema import DocumentRequest

router = APIRouter()


@router.post("")
async def upload_file(
    document_request: DocumentRequest = Depends(validate_upload),
    document_service: DocumentService = Depends(select_loader),

) ->  Document:
    # Check file extension

    # Read file content into memory

    result = await document_service.add_document(document_request.content)

    return result
