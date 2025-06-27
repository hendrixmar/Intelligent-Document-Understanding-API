# repositories/vector_store.py
from abc import ABC, abstractmethod
from typing import List

from rag.domain.models.document import Document, DocumentCategory


class BaseDocumentClassifier(ABC):
    """
    Abstract base class for document classification.

    This class defines the interface for asynchronously assigning a document
    to a specific cluster or category based on its content. Implementations
    may use rule-based logic, traditional machine learning, or large language
    models (LLMs) to determine the most appropriate classification.

    Subclasses must implement the `clustering` method to provide their own
    classification strategy.
    """

    @abstractmethod
    async def clustering(self, document: Document) -> DocumentCategory | None:
        """
        Asynchronously classify a document into a cluster or category.

        Parameters:
            document (str): The input document content as a plain text string.

        Returns:
            str: The name or identifier of the assigned cluster or category.
        """
        pass
