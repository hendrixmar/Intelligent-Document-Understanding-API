from abc import ABC, abstractmethod



class BaseEntityExtractor(ABC):

    @abstractmethod
    async def extract_entities(self, input_text: str) -> dict[str, list[str]]:
        """Add documents with optional metadata to the vector store."""

