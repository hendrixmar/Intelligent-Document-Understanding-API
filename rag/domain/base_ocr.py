from abc import ABC, abstractmethod
import numpy as np


class BaseOpticalCharacterRecognizer(ABC):
    """
    Abstract base class for optical character recognition (OCR) systems.

    This interface defines the contract for implementing OCR methods that
    extract text from processed image data. The OCR engine is expected to
    operate on images (typically preprocessed) and return a list of detected
    text strings.

    Subclasses must implement the `detect_character` method to apply OCR logic
    according to specific libraries or models (e.g., EasyOCR, Tesseract, custom LLMs).
    """

    @abstractmethod
    def detect_character(self, image: np.ndarray, settings: dict | None = None) -> list[str]:
        """
        Detect and extract text characters from the given image.

        Parameters:
            image (np.ndarray): The input image as a NumPy array, usually preprocessed
                                (e.g., binarized, denoised, or contrast-adjusted).
            settings (dict | None): Optional configuration parameters for the OCR engine,
                                    such as language, detail level, or thresholds.

        Returns:
            list[str]: A list of recognized text strings extracted from the image.
        """
        ...
