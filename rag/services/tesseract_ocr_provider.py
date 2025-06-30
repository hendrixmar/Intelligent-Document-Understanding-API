import re

import numpy as np
import os

from rag.domain.base_ocr import BaseOpticalCharacterRecognizer
import cv2
import pytesseract
# Load image



class TesseractProvider(BaseOpticalCharacterRecognizer):

    def __init__(self):
        if os.name == 'nt':
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


    def detect_character(
        self,
        image: np.ndarray,
        settings: dict | None = None
    ) -> str:
        return " ".join(
            re.sub(r"[^\w\s.,;:-]", "", e).strip()
           for e in pytesseract.image_to_string(image).split()
        )
