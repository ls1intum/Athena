import json
from typing import TypeVar, Generic, Optional

import httpx
from fastapi import HTTPException
from pydantic.generics import GenericModel

from .module import Module
from .available_module_enum import AvailableModuleNames
from .list_modules import list_modules
from assessment_module_manager import env

T = TypeVar('T')
M = TypeVar('M')
class ModuleResponse(GenericModel, Generic[T, M]):
    """
    A response from a module.
    """
    module_name: str
    status: int
    data: T
    meta: M


async def find_module_by_name(
    module_name: AvailableModuleNames  # type: ignore
) -> Optional[Module]:
    """
    Helper function to find a module by name.
    """
    for module in list_modules():
        if module.name == module_name:
            return module
    return None


async def request_to_module(module: Module, module_config: Optional[str], path: str, data: Optional[dict], method: str) -> ModuleResponse:
    """
    Helper function to send a request to a module.
    It raises appropriate FastAPI HTTPException if the request fails.
    """
    module_secret = env.MODULE_SECRETS[module.name]
headers = {}
if module_secret:
    headers['X-API-Secret'] = module_secret
if module_config:
    headers['X-Module-Config'] = module_config

    try:
        async with httpx.AsyncClient(base_url=module.url, timeout=600) as client:
            if method == "POST":
                response = await client.post(path, json=data, headers=headers)
            else:
                response = await client.get(path, headers=headers)
    except httpx.ConnectError as exc:
        raise HTTPException(status_code=503, detail=f"Module {module.name} is not available") from exc
    
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError:
        pass

    try:
        response_data = response.json()
        meta = response_data.get('meta', {})
        response_data = response_data.get('data', response_data)
    except json.JSONDecodeError:
        response_data = response.text
        meta = {}
    return ModuleResponse(module_name=module.name, status=response.status_code, data=response_data, meta=meta)