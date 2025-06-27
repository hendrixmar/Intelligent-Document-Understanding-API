# repositories/vector_store.py
from abc import ABC, abstractmethod
from typing import List


class VectorStoreRepository(ABC):

    @abstractmethod
    async def add_documents(self, documents: List[dict]) -> None:
        """Add documents with optional metadata to the vector store."""

    @abstractmethod
    async def similarity_search(self, query: str, k: int = 5) -> List[str]:
        """Return top-k documents relevant to the query."""
