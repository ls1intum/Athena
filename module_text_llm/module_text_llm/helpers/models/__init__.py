import os
from . import openai # noqa
from .model_factory import model_factory
from athena.logger import logger
import openai
openai.debug = True # delete later

available_models = list(model_factory.model_builders.keys())

default_model_key = os.environ.get("LLM_DEFAULT_MODEL")
if default_model_key is None or default_model_key not in available_models:
    raise EnvironmentError(f"LLM_DEFAULT_MODEL is not set correctly, available models:\n{', '.join(available_models)}")


logger.info(f"Using default model: {default_model_key}")

get_default_model = model_factory.model_builders[default_model_key]
logger.info(f"get_default_model: {get_default_model()}")


logger.info(openai.api_type) # delete later
logger.info(openai.api_key) # delete later
logger.info(openai.api_base) # delete later
logger.info(openai.api_version) # delete later

__all__ = [
    "available_models",
    "model_factory",
    "get_default_model",
]
