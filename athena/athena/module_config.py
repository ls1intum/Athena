import configparser
from dataclasses import dataclass
import json
from typing import Dict, Optional

from fastapi import HTTPException, Header, status

from .schemas.exercise_type import ExerciseType


@dataclass
class ModuleConfig:
    """Config from module.conf."""
    name: str
    type: ExerciseType
    port: int


def get_module_config() -> ModuleConfig:
    """Get the module from the config file."""
    config = configparser.ConfigParser()
    config.read("module.conf")
    return ModuleConfig(
        name=config["module"]["name"],
        type=ExerciseType(config["module"]["type"]),
        port=int(config["module"]["port"]),
    )


async def get_dynamic_module_config(module_config: Optional[str] = Header(None, alias="X-Module-Config")) -> Optional[Dict]:
    """Get the dynamic module config from the request header."""
    if module_config is not None:
        try:
            return json.loads(module_config)
        except json.JSONDecodeError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="Invalid module config received, check the X-Module-Config header")
    return None