from rag.domain.base_chunker import BaseChunker
from rag.domain.base_classifier import BaseDocumentClassifier
from rag.domain.base_document_loader import BaseDocumentLoader
from rag.domain.base_entity_extraction import BaseEntityExtractor
from rag.domain.base_vector_store import VectorStoreRepository
from kink import inject

@inject
class DocumentService:

    def __init__(
        self,
        document_loader: BaseDocumentLoader,
        vector_store: VectorStoreRepository,
        document_classifier: BaseDocumentClassifier,
        entity_extractor: BaseEntityExtractor,
        document_chunker: BaseChunker,
    ):
        self.document_loader = document_loader
        self.vector_store = vector_store
        self.entity_extractor = entity_extractor
        self.document_classifier = document_classifier
        self.document_chunker = document_chunker

    async def add_document(self, raw_document: bytes):

        document = self.document_loader.load(raw_document)

        for page in document.pages:
            document_chunks = await self.document_chunker.split_documents(page.content)
            page.chunks.extend(document_chunks)

        results  = await self.document_classifier.clustering(
            document
        )
        document.category = results
        for page in document.pages:
            for chunk in page.chunks:
                result = await self.entity_extractor.extract_entities(chunk.text)
                chunk.metadata.update(
                    {
                        "entities": result,
                        "document_name":document.title,
                        "document_type": results.value

                    }
                )


        for page in document.pages:
            await self.vector_store.add_documents(
                [{**chunk.metadata, "document_content": chunk.text} for chunk in page.chunks]
            )


        return [{"key": str(results)}]






