from fastapi.routing import APIRouter

from rag.web.api import extract_entities, document

api_router = APIRouter()
api_router.include_router(document.router, prefix="/documents", tags=["ml"])
api_router.include_router(extract_entities.router, prefix="/extract_entities", tags=["ml"])
