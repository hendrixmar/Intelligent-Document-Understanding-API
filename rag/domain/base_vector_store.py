# repositories/vector_store.py
from abc import ABC, abstractmethod
from typing import List


class VectorStoreRepository(ABC):
    """
    Abstract base class for interacting with a vector store.

    This interface defines the required methods for storing and retrieving documents
    using vector-based similarity search. Implementations should manage the embedding,
    storage, and querying of documents in a vector database.

    Common use cases include semantic search, question answering, and retrieval-augmented generation (RAG).
    """

    @abstractmethod
    async def add_documents(self, documents: List[dict]) -> None:
        """
        Add documents with optional metadata to the vector store.

        Parameters:
            documents (List[dict]): A list of documents, where each document is a dictionary
                                    that may contain keys like 'text', 'metadata', etc.

        Returns:
            None
        """
        ...

    @abstractmethod
    async def similarity_search(self, query: str, k: int = 5) -> List[dict]:
        """
        Perform a similarity search against the vector store using the given query.

        Parameters:
            query (str): The input query string to search for relevant documents.
            k (int): The number of top matching documents to return. Default is 5.

        Returns:
            List[dict]: A list of top-k document contents ranked by similarity to the query.
        """
        ...
