import os

from langchain.base_language import BaseLanguageModel

from .openai import available_models as available_openai_models
from .openai import OpenAIModelConfig


model_config = OpenAIModelConfig

# model names -> models
available_models: dict[str, BaseLanguageModel] = {
    **available_openai_models,
}

default_model_key = os.environ.get("LLM_DEFAULT_MODEL")
if default_model_key is None or default_model_key not in available_models:
    raise EnvironmentError(f"LLM_DEFAULT_MODEL is not set correctly, available models:\n{', '.join(available_models)}")

model = available_models[default_model_key]


__all__ = [
    "model_config",
    "available_models",
    "model",
]
