import os
from .openai import available_models as available_openai_models


available_models = {
    **available_openai_models,
}

default_model_key = os.environ.get("LLM_DEFAULT_MODEL")
if default_model_key is None or default_model_key not in available_models:
    raise EnvironmentError(f"LLM_DEFAULT_MODEL is not set correctly, available models:\n{', '.join(available_models)}")

model = available_models[default_model_key]

__all__ = [
    "available_models",
    "model",
]
