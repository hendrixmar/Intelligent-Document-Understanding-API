from abc import ABC, abstractmethod

from rag.domain.models.document import DocumentCategory


class BaseEntityExtractor(ABC):

    @abstractmethod
    async def extract_entities(self, input_text: str, category: DocumentCategory) -> dict[str, list[str]]:
        """Add documents with optional metadata to the vector store."""

