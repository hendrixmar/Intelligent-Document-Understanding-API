from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes
import io


from rag.domain.base_document_loader import BaseDocumentLoader
from rag.domain.base_image_preprocess import BaseImagePreprocess
from rag.domain.base_ocr import BaseOpticalCharacterRecognizer
from rag.domain.models.document import Document, DocumentMetadata
from rag.domain.models.page import Page
from PyPDF2 import PdfReader
from kink import inject

def get_pdf_metadata_from_bytes(pdf_bytes: bytes) -> dict:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    metadata = reader.metadata
    return {
        "title": metadata.title,
        "author": metadata.author,
        "subject": metadata.subject,
        "creator": metadata.creator,
        "producer": metadata.producer,
        "creation_date": metadata.creation_date,
        "modification_date": metadata.modification_date,
        "number_of_pages": len(reader.pages),
        "file_type": "pdf",
        "file_size": len(pdf_bytes)
    }


def _pil_image_to_bytes(pil_img: Image.Image, _format: str = "PNG") -> bytes:
    buf = io.BytesIO()
    pil_img.save(buf, format=_format)
    return buf.getvalue()

@inject
class PdfLoader(BaseDocumentLoader):

    def __init__(
        self,
        image_preprocess: BaseImagePreprocess,
        ocr_provider: BaseOpticalCharacterRecognizer

    ):
        self.preprocess_provider = image_preprocess
        self.ocr_provider = ocr_provider


    def load(self, raw_document: bytes) -> Document:

        pages: list[Image.Image] = convert_from_bytes(raw_document)
        metadata = get_pdf_metadata_from_bytes(raw_document)

        return Document(
            title=metadata.get("title"),
            metadata=DocumentMetadata.model_validate(metadata),
            pages=[
                self._scan_page(page, i) for i, page in enumerate(pages, 1)
            ]
        )


    def _scan_page(self, page: Image, number: int) -> Page:
        raw_page = _pil_image_to_bytes(page)
        preprocessed = self.preprocess_provider.preprocess_image(raw_page)
        page_text = self.ocr_provider.detect_character(preprocessed)



        return Page(number=number, content="\n".join(page_text))

