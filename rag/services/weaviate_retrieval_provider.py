from typing import AsyncGenerator

import weaviate
from fastapi import Depends
from weaviate import WeaviateAsyncClient

from rag.domain.base_entities_extraction import VectorStoreRepository


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


class WeaviateRetrievalProvider(VectorStoreRepository):
    def __init__(self, client: WeaviateAsyncClient = Depends(get_db_session)):
        self.async_client = client
        self.documents_collection = client.collections.get("WineReviews")

    async def add_documents(self, documents: list[dict]) -> str:
        """Add documents with optional metadata to the vector store."""

        response = await self.documents_collection.data.insert_many(documents)
        return str(response)

    async def similarity_search(self, query: str, k: int = 5) -> list[str]:
        """Return top-k documents relevant to the query."""
        response = await self.documents_collection.query.near_text(
            include_vector=True,
            query=query,
            limit=k,
            return_metadata=[
                "creation_time",
                "last_update_time",
                "distance",
                "certainty",
                "score",
                "explain_score",
                "is_consistent",
            ],
        )

        return [e.properties for e in response.objects]
