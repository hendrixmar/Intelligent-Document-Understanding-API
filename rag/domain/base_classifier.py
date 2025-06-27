# repositories/vector_store.py
from abc import ABC, abstractmethod
from typing import List


class BaseDocumentClassifier(ABC):

    @abstractmethod
    async def clustering(self, document: str) -> str:
        """Add documents with optional metadata to the vector store."""
