from PIL import Image
import io


from rag.domain.base_document_loader import BaseDocumentLoader
from rag.domain.base_image_preprocess import BaseImagePreprocess
from rag.domain.base_ocr import BaseOpticalCharacterRecognizer
from rag.domain.models.document import Document, DocumentMetadata
from rag.domain.models.page import Page
from kink import inject

@inject
class ImageLoader(BaseDocumentLoader):

    def __init__(
        self,
        image_preprocess: BaseImagePreprocess,
        ocr_provider: BaseOpticalCharacterRecognizer

    ):
        self.preprocess_provider = image_preprocess
        self.ocr_provider = ocr_provider


    def load(self, raw_document: bytes) -> Document:

        return Document(
            title="unknowing",
            metadata=None,
            pages=[
                self._scan_page(raw_document, 1)
            ]
        )


    def _scan_page(self, raw_page: bytes, number: int) -> Page:
        preprocessed = self.preprocess_provider.preprocess_image(raw_page)
        page_text = self.ocr_provider.detect_character(preprocessed)

        return Page(number=number, content="\n".join(page_text))

