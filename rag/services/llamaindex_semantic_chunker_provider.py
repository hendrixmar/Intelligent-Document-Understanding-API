
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.node_parser import (
    SemanticSplitterNodeParser,
)
from llama_index.core.readers import StringIterableReader

from rag.domain.base_chunker import BaseChunker
from rag.domain.models.chunk import Chunk


class LlamaIndexSemanticChunker(BaseChunker):

    def __init__(self, embedder_model: BaseEmbedding):
        self.splitter = SemanticSplitterNodeParser(
            buffer_size=1,
            breakpoint_percentile_threshold=95,
            embed_model=embedder_model,
        )

    async def split_documents(self, text: str) -> list[Chunk]:
        """Add documents with optional metadata to the vector store."""

        document = StringIterableReader().load_data([text])
        nodes = await self.splitter.aget_nodes_from_documents(document)
        return [Chunk(text=e.get_content()) for e in nodes]
