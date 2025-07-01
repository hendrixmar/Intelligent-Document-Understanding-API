from typing import AsyncGenerator

import weaviate
from fastapi import Depends
from weaviate import WeaviateAsyncClient
from weaviate.collections.classes.grpc import MetadataQuery

from rag.domain.base_vector_store import VectorStoreRepository


async def get_db_session() -> AsyncGenerator[WeaviateAsyncClient, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    client = weaviate.use_async_with_local(
        host="weaviate",
        port=8080,
    )

    try:
        await client.connect()
        yield client
    finally:
        await client.close()

class DocumentWeaviateRepository(VectorStoreRepository):
    """
    Repository for interacting with the Weaviate vector database for document storage and retrieval.

    This class provides methods to insert documents with metadata (including entity handling)
    and perform similarity searches based on a query string.

    Attributes:
        async_client (WeaviateAsyncClient): The asynchronous Weaviate client instance.
        documents_collection: The 'Documents' collection from the Weaviate client.
    """

    def __init__(self, client: WeaviateAsyncClient = Depends(get_db_session)):
        """
        Initialize the repository with an async Weaviate client.

        Args:
            client (WeaviateAsyncClient): The injected Weaviate async client dependency.
        """
        self.async_client = client
        self.documents_collection = client.collections.get("Documents")

    async def add_documents(self, documents: list[dict]) -> None:
        """
        Add a list of documents to the Weaviate vector store.

        This method checks if any document includes an entity field `"date"`, and if so,
        it renames it to `"current_date"` to avoid schema mismatches.

        Args:
            documents (list[dict]): A list of document dictionaries containing metadata and content.
        """

        await self.documents_collection.data.insert_many(documents)

    async def similarity_search(self, query: str, k: int = 5) -> list[dict]:
        """
        Perform a hybrid similarity search on the 'Documents' collection.

        Combines vector and keyword search using a weighted hybrid approach.

        Args:
            query (str): The search query string.
            k (int): The number of top results to return. Defaults to 5.

        Returns:
            list[dict]: A list of matching documents with their metadata and similarity scores.
        """
        response = await self.documents_collection.query.hybrid(
            query=query,
            limit=k,
            alpha=0.5,
            return_metadata=MetadataQuery(score=True, explain_score=True)
        )

        return [
            {
                **e.properties,
                "score": e.metadata.score,
                "explain_score": e.metadata.explain_score
            }
            for e in response.objects
        ]
