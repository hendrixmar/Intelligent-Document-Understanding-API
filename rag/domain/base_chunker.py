# repositories/vector_store.py
from abc import ABC, abstractmethod


class BaseChunker(ABC):

    @abstractmethod
    async def split_documents(self, text: str) -> list[str]:
        """Add documents with optional metadata to the vector store."""
