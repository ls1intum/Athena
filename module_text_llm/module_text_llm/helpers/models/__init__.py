import os

from langchain.base_language import BaseLanguageModel

from .openai import available_models as available_openai_models
from .openai import OpenAIModelSettings


# model names -> models
available_models: dict[str, BaseLanguageModel] = {
    **available_openai_models,
}

default_model_key = os.environ.get("LLM_DEFAULT_MODEL")
if default_model_key is None or default_model_key not in available_models:
    raise EnvironmentError(f"LLM_DEFAULT_MODEL is not set correctly, available models:\n{', '.join(available_models)}")

model = available_models[default_model_key]


provider_to_model_settings = {
    "openai": OpenAIModelSettings,
}


def get_model(provider: str, settings: dict) -> BaseLanguageModel:
    """Get a model from a provider and settings.

    Args:
        provider (str): The provider to use.
        settings (dict): The settings to use. (See provider_to_model_settings)

    Raises:
        ValueError: If the provider is not supported or the settings are invalid.

    Returns:
        BaseLanguageModel: The model.
    """    
    if provider not in provider_to_model_settings:
        raise ValueError(f"Provider {provider} is not supported, available providers: {', '.join(provider_to_model_settings)}.")
    
    model_config = provider_to_model_settings[provider](**settings)
    if not isinstance(model_config.model_name, str):
        raise ValueError(f"Model name must be a string, got {model_config.model_name} of type {type(model_config.model_name)}.")
    if model_config.model_name not in available_models:
        raise ValueError(f"Model {model_config.model_name} is not supported, available models: {', '.join(available_models)}.")
    model = available_models[model_config.model_name].copy()
    for attr, value in model_config.__dict__.items():
        setattr(model, attr, value)
    return model


__all__ = [
    "provider_to_model_settings",
    "available_models",
    "model",
    "get_model",
]
