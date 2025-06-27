import io
import cv2
import numpy as np
from PIL import Image

from rag.domain.base_image_preprocess import BaseImagePreprocess
from rag.utils import fastapi_exception_handler


class StandardImagePreprocess(BaseImagePreprocess):

    @fastapi_exception_handler
    def preprocess_image(self, image: bytes) -> np.ndarray:
        image_stream = io.BytesIO(image)

        pil_image = Image.open(image_stream)
        image = np.array(pil_image)

        if len(image.shape) == 3 and image.shape[2] == 3:
            code = cv2.COLOR_BGR2GRAY if image.shape[2] == 3 else cv2.COLOR_RGB2GRAY
            gray = cv2.cvtColor(image, code)
        elif len(image.shape) == 2:  # already grayscale
            gray = image
        else:
            raise ValueError(f"Unexpected image shape: {image.shape}")

        # Resize, denoise, threshold
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15,
        )
        denoised = cv2.fastNlMeansDenoising(thresh, None, 30, 7, 21)
        scaled = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        morphed = cv2.morphologyEx(scaled, cv2.MORPH_CLOSE, kernel)

        return morphed
