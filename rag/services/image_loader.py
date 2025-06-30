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
    """
    A document loader that processes image-based documents using a preprocessing step
    and OCR (Optical Character Recognition) to extract text.

    Attributes:
        preprocess_provider (BaseImagePreprocess): A service that handles image preprocessing.
        ocr_provider (BaseOpticalCharacterRecognizer): A service that performs OCR to extract text.
    """

    def __init__(
        self,
        image_preprocess: BaseImagePreprocess,
        ocr_provider: BaseOpticalCharacterRecognizer
    ):
        """
        Initialize the ImageLoader with preprocessing and OCR providers.

        Args:
            image_preprocess (BaseImagePreprocess): The image preprocessing implementation.
            ocr_provider (BaseOpticalCharacterRecognizer): The OCR implementation for text extraction.
        """
        self.preprocess_provider = image_preprocess
        self.ocr_provider = ocr_provider

    def load(self, raw_document: bytes) -> Document:
        """
        Load and process a single image document from raw bytes.

        The image is preprocessed, OCR is applied, and the result is wrapped
        into a Document with a single Page.

        Args:
            raw_document (bytes): The raw image data to be processed.

        Returns:
            Document: A structured document containing the OCR-extracted text.
        """
        return Document(
            title="unknowing",  # This could be made dynamic in a full implementation
            metadata=None,
            pages=[
                self._scan_page(raw_document, 1)
            ]
        )

    def _scan_page(self, raw_page: bytes, number: int) -> Page:
        """
        Process a single page of the document by applying preprocessing and OCR.

        Args:
            raw_page (bytes): Raw image bytes of the page.
            number (int): Page number in the document.

        Returns:
            Page: A page object containing the extracted text content.
        """
        preprocessed = self.preprocess_provider.preprocess_image(raw_page)
        page_text = self.ocr_provider.detect_character(preprocessed)
        return Page(number=number, content=page_text)

