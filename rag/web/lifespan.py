from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from kink import di
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

from rag.create_database import create_database
from rag.domain.base_chunker import BaseChunker
from rag.domain.base_classifier import BaseDocumentClassifier
from rag.domain.base_entity_extraction import BaseEntityExtractor
from rag.domain.base_image_preprocess import BaseImagePreprocess
from rag.domain.base_ocr import BaseOpticalCharacterRecognizer

from rag.exception_handler import fastapi_exception_handler
from rag.services.llamaindex_document_classifier import LlamaIndexDocumentClassifier
from rag.services.llamaindex_entity_extraction import LlamaIndexEntityExtractor
from rag.services.llamaindex_semantic_chunker_provider import LlamaIndexSemanticChunker
from rag.services.standard_preprocess import StandardImagePreprocess
from rag.services.tesseract_ocr_provider import TesseractProvider
from rag.settings import settings


@asynccontextmanager
async def lifespan_setup(
    app: FastAPI,
) -> AsyncGenerator[None, None]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """
    fastapi_exception_handler(app)
    create_database()
    app.middleware_stack = None
    app.middleware_stack = app.build_middleware_stack()
    create_dependency_container()
    yield


def create_dependency_container():
    llm = OpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key=settings.openai_api_key
    )
    embeder = OpenAIEmbedding(api_key=settings.openai_api_key)

    di[BaseImagePreprocess] = StandardImagePreprocess()
    di[BaseOpticalCharacterRecognizer] = TesseractProvider()
    di[BaseEntityExtractor] = LlamaIndexEntityExtractor(llm)
    di[BaseChunker] = LlamaIndexSemanticChunker(embeder)
    di[BaseDocumentClassifier] = LlamaIndexDocumentClassifier(llm)
