import functools

from PIL import UnidentifiedImageError
from fastapi import HTTPException


def fastapi_exception_handler(func):
    @functools.wraps(func)
    def wrapper (*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UnidentifiedImageError as e:
            raise HTTPException(status_code=400, detail=f"Invalid image format. {e}")
        except ValueError as ve:
            raise HTTPException(status_code=422, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    return wrapper
