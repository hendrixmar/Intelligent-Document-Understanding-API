from abc import ABC, abstractmethod
import numpy as np

class BaseImagePreprocess(ABC):
    """
    Abstract base class for image preprocessing routines.

    This interface defines the contract for implementing image preprocessing steps
    aimed at enhancing features or preparing the image for tasks such as OCR
    (optical character recognition), document analysis, or computer vision pipelines.

    Subclasses must implement the `detect_character` method, which processes an image
    to highlight or isolate characters or text regions.
    """

    @abstractmethod
    def preprocess_image(self, image: bytes) -> np.ndarray:
        """
        Process an image to enhance or detect character regions.

        Parameters:
            image (bytes): The input image as a byte stream (e.g., JPEG or PNG data).

        Returns:
            np.ndarray: A processed NumPy array representing the modified image,
                        typically in grayscale or binary format suitable for OCR or
                        further analysis.
        """
        ...
