# repositories/vector_store.py
from abc import ABC, abstractmethod

class BaseChunker(ABC):
    """
    Abstract base class for text chunkers.

    This class defines the interface for asynchronously splitting a large text
    into smaller chunks, which can be used for downstream processing such as
    indexing, embedding, or retrieval in vector databases or language models.

    Subclasses must implement the `split_documents` method with their own
    chunking logic (e.g., based on length, sentences, tokens, or semantic boundaries).
    """

    @abstractmethod
    async def split_documents(self, text: str) -> list[str]:
        """
        Asynchronously split a single input text into a list of smaller text chunks.

        Parameters:
            text (str): The input text to be split.

        Returns:
            list[str]: A list of strings, each representing a chunk of the original text.
        """
        pass
