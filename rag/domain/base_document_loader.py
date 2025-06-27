from abc import ABC, abstractmethod
from PIL import Image

from rag.domain.models.document import Document


class BaseDocumentLoader(ABC):
    """
    Abstract base class for document loaders.

    This interface defines a common method for loading documents of various formats
    (e.g., PDF, JPEG, PNG, DOCX) and extracting their content into a standardized
    text representation.

    Subclasses must implement the `load` method to handle the specific logic of
    parsing and converting the source file into a plain text string or appropriate format
    for downstream tasks such as analysis, indexing, or classification.
    """

    @abstractmethod
    def load(self, raw_image: bytes) -> Document:
        """
        Load the document and extract its main textual content.

        Returns:
            str: A plain text string representing the content of the document.
        """
        pass
