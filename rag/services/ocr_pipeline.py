import re
from typing import List

import cv2
import easyocr
import numpy as np
from PIL import Image


def preprocess_image(pil_image: Image.Image) -> np.ndarray:
    """
    Preprocess a PIL image for OCR by converting to grayscale, resizing, denoising, and thresholding.

    Args:
        pil_image (Image.Image): Input image in PIL format.

    Returns:
        np.ndarray: Preprocessed binary image suitable for OCR.
    """
    # Convert to OpenCV format (NumPy array)
    image = np.array(pil_image)

    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 2:  # already grayscale
        gray = image
    else:
        raise ValueError(f"Unexpected image shape: {image.shape}")

    # Resize, denoise, threshold
    # gray = cv2.resize(gray, (0, 0), fx=1.5, fy=1.5)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15,
    )
    denoised = cv2.fastNlMeansDenoising(thresh, None, 30, 7, 21)
    scaled = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    morphed = cv2.morphologyEx(scaled, cv2.MORPH_CLOSE, kernel)

    return morphed


def run_easyocr_on_image(image: np.ndarray) -> List[str]:
    """
    Run EasyOCR on a preprocessed image and return cleaned extracted text.

    Args:
        image (np.ndarray): Preprocessed image as a NumPy array.

    Returns:
        List[str]: List of cleaned text strings extracted from the image.
    """
    reader = easyocr.Reader(["en"], gpu=True)
    results = reader.readtext(
        image,  # Or whatever final preprocessed image
        detail=1,
        paragraph=True,
        contrast_ths=0.05,
        adjust_contrast=0.5,
        text_threshold=0.3,
        low_text=0.3,
        link_threshold=0.4,
    )

    cleaned = [re.sub(r"[^\w\s.,;:-]", "", text[1]).strip() for text in results]
    return cleaned
