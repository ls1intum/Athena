import os

from athena.logger import logger
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader

load_dotenv(".env")
SECRET = os.getenv("SECRET")
DEBUG = os.environ["PRODUCTION"] == "0"

api_key_header = APIKeyHeader(name='X-API-Secret', auto_error=False)


def verify_secret(secret: str):
    """
    To use this function, add this param to your FastAPI route:
    auth=Depends(authenticate)
    """
    if secret != SECRET:
        if DEBUG:
            logger.warning("DEBUG MODE: Ignoring invalid API secret.")
        else:
            raise HTTPException(status_code=401, detail="Invalid API secret.")
