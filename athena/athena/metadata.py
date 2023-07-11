from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from typing import Dict, Any
import contextvars


metadata_context: contextvars.ContextVar[Dict[str, Any]] = contextvars.ContextVar("metadata")


class MetaDataMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # Init metadata in context variable
        metadata_context.set({})
        response = await call_next(request)
        return response


def get_meta() -> Dict[str, Any]:
    # This will return an empty dict if no metadata has been set
    return metadata_context.get({})


def emit_meta(key: str, value: Any):
    # Get the current metadata, add the new key-value pair
    metadata = metadata_context.get({})
    metadata[key] = value
