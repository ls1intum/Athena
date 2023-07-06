import os
from .openai import available_models as openai_available_models
from langchain.base_language import BaseLanguageModel


available_models: dict[str, BaseLanguageModel] = openai_available_models

default_model_key = os.environ.get("LLM_DEFAULT_MODEL")
if default_model_key is None:
    raise EnvironmentError(f"LLM_DEFAULT_MODEL is not set, available models: {available_models.keys()}")
model = available_models[default_model_key]

__all__ = [
    "available_models",
    "model", # default model
]
