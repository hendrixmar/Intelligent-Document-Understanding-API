from rag.services.easy_ocr_provider import EasyOCRProvider
from rag.services.standard_preprocess import StandardImagePreprocess

class DocumentService:



    def __init__(self, ):
        pass
    async def add_document(self, raw_document: bytes):
        ocr_provider = EasyOCRProvider()
        preprocess_provider = StandardImagePreprocess()
        all_text = []
        for page in document:
            preprocessed = preprocess_provider.preprocess_image(
                load(page))
            page_text = ocr_provider.detect_character(preprocessed)
        # Cargar todos los documentos de la carpeta raiz
        # Extraer el text con
        # OCR pipeline
        # llamaindex_semantic_chunker
        # por cada chunk exrtraemos entidades
        # le ponemos su categoria
        # utilizamos knn para saber la categoria de todo el documento
        #metemos el documento a la base con base_vector

        ...
