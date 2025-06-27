import re
from typing import TypedDict

import easyocr
import numpy as np

from rag.domain.base_ocr import BaseOpticalCharacterRecognizer


class EasyOCRConfig(TypedDict):
    detail: int
    paragraph: bool
    contrast_ths: float
    adjust_contrast: float
    text_threshold: float
    low_text: float
    link_threshold: float


class EasyOCRProvider(BaseOpticalCharacterRecognizer):

    def __init__(self):
        self.reader = easyocr.Reader(["en"], gpu=True)
        self.default_settings = dict(detail=1,
                                     paragraph=True,
                                     contrast_ths=0.05,
                                     adjust_contrast=0.5,
                                     text_threshold=0.3,
                                     low_text=0.3,
                                     link_threshold=0.4)

    def detect_character(
        self,
        image: np.ndarray,
        settings: EasyOCRConfig | None = None
    ) -> list[str]:

        results = self.reader.readtext(
            image,  # Or whatever final preprocessed image
            **(settings if settings else self.default_settings)
        )

        cleaned = [re.sub(r"[^\w\s.,;:-]", "", text[1]).strip() for text in results]
        return cleaned
