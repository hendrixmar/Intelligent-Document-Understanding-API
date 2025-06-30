from PIL import UnidentifiedImageError
from fastapi import FastAPI, Request
from pytesseract import pytesseract
from fastapi.responses import JSONResponse
from weaviate.exceptions import WeaviateInsertManyAllFailedError


def fastapi_exception_handler(app: FastAPI):
    @app.exception_handler(WeaviateInsertManyAllFailedError)
    async def tesseract_not_found_handler(request: Request,
                                          exc: ValueError):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)}
        )
    @app.exception_handler(ValueError)
    async def tesseract_not_found_handler(request: Request,
                                          exc: ValueError):
        return JSONResponse(
            status_code=422,
            content={"detail": str(exc)}
        )

    @app.exception_handler(UnidentifiedImageError)
    async def tesseract_not_found_handler(request: Request,
                                          exc: UnidentifiedImageError):
        return JSONResponse(
            status_code=500,
            content={"detail": f"Invalid image format. {exc}"}
        )

    @app.exception_handler(pytesseract.TesseractNotFoundError)
    async def tesseract_not_found_handler(request: Request,
                                          exc: pytesseract.TesseractNotFoundError):
        return JSONResponse(
            status_code=500,
            content={"detail": "Tesseract is not installed or not found."}
        )

    @app.exception_handler(pytesseract.TesseractError)
    async def tesseract_error_handler(request: Request,
                                      exc: pytesseract.TesseractError):
        return JSONResponse(
            status_code=500,
            content={"detail": f"Tesseract OCR error: {str(exc)}"}
        )
