import os
from contextlib import contextmanager

import openai
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.llms import AzureOpenAI, OpenAI
from langchain.base_language import BaseLanguageModel

from athena.logger import logger

from .model_factory import model_factory


openai_available = os.environ.get("LLM_OPENAI_API_KEY") is not None
azure_openai_available = os.environ.get("LLM_AZURE_OPENAI_API_KEY") is not None


def set_azure():
    openai.api_type = "azure"
    openai.api_key = os.environ.get("LLM_AZURE_OPENAI_API_KEY")
    openai.api_base = os.environ.get("LLM_AZURE_OPENAI_API_BASE")
    openai.api_version = "2022-06-01-preview" # os.environ.get("LLM_AZURE_OPENAI_API_VERSION")

def set_openai():
    openai.api_type = "open_ai"
    openai.api_key = os.environ.get("LLM_OPENAI_API_KEY")
    openai.api_base = "https://api.openai.com/v1"
    openai.api_version = None



# This is a hack to make sure that the openai api is set correctly
# Right now it is overkill, but it will be useful when the api gets fixed and we no longer
# hardcode the model names
@contextmanager
def openai_client(use_azure_api: bool, is_preference: bool):
    """Set the openai client to use the correct api type, if available

    Args:
        use_azure_api (bool): If true, use the azure api, else use the openai api
        is_preference (bool): If true, it can fall back to the other api if the preferred one is not available
    """
    original_api_type = openai.api_type
    original_api_key = openai.api_key
    original_api_base = openai.api_base
    original_api_version = openai.api_version

    if use_azure_api:
        if azure_openai_available:
            set_azure()
        elif is_preference and openai_available:
            set_openai()
        elif is_preference:
            raise EnvironmentError(
                "No OpenAI api available, please set LLM_AZURE_OPENAI_API_KEY, LLM_AZURE_OPENAI_API_BASE and LLM_AZURE_OPENAI_API_VERSION environment variables or LLM_OPENAI_API_KEY environment variable")
        else:
            raise EnvironmentError(
                "Azure OpenAI api not available, please set LLM_AZURE_OPENAI_API_KEY, LLM_AZURE_OPENAI_API_BASE and LLM_AZURE_OPENAI_API_VERSION environment variables")
    else:
        if openai_available:
            set_openai()
        elif is_preference and azure_openai_available:
            set_azure()
        elif is_preference:
            raise EnvironmentError(
                "No OpenAI api available, please set LLM_OPENAI_API_KEY environment variable or LLM_AZURE_OPENAI_API_KEY, LLM_AZURE_OPENAI_API_BASE and LLM_AZURE_OPENAI_API_VERSION environment variables")
        else:
            raise EnvironmentError(
                "OpenAI api not available, please set LLM_OPENAI_API_KEY environment variable")

    yield

    openai.api_type = original_api_type
    openai.api_key = original_api_key
    openai.api_base = original_api_base
    openai.api_version = original_api_version


# Hardcoded because openai can't provide a trustworthly api to get the list of models and capabilities...
openai_models = {
    "chat_completion": [
        "gpt-4",
        "gpt-4-32k",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k"
    ],
    "completion": [
        "text-davinci-003",
        "text-curie-001",
        "text-babbage-001",
        "text-ada-001",
    ],
    "fine_tuneing": [
        "davinci",
        "curie",
        "babbage",
        "ada",
    ]
}

available_deployments: dict = {
    "chat_completion": {},
    "completion": {},
    "fine_tuneing": {},
}

if azure_openai_available:
    with openai_client(use_azure_api=True, is_preference=False):
        deployments = openai.Deployment.list().get("data")  # type: ignore
        if deployments is not None:
            for deployment in deployments:
                # special case for gpt-3.5-turbo...
                if deployment.model in openai_models["chat_completion"] or deployment.model == "gpt-35-turbo":
                    available_deployments["chat_completion"][deployment.id] = deployment
                elif deployment.model in openai_models["completion"]:
                    available_deployments["completion"][deployment.id] = deployment
                elif deployment.model in openai_models["fine_tuneing"]:
                    available_deployments["fine_tuneing"][deployment.id] = deployment


available_models: dict[str, BaseLanguageModel] = {}

if openai_available:
    openai_api_key = os.environ["LLM_OPENAI_API_KEY"]
    for model_name in openai_models["chat_completion"]:
        model_factory.register_model(f"openai_{model_name}",
                                     lambda model_name=model_name:
                                     ChatOpenAI(model=model_name, openai_api_key=openai_api_key, client=""))
    for model_name in openai_models["completion"]:
        model_factory.register_model(f"openai_{model_name}",
                                     lambda model_name=model_name:
                                     OpenAI(model=model_name, openai_api_key=openai_api_key, client=""))

if azure_openai_available:
    azure_openai_api_key = os.environ["LLM_AZURE_OPENAI_API_KEY"]
    azure_openai_api_base = os.environ["LLM_AZURE_OPENAI_API_BASE"]
    azure_openai_api_version = os.environ["LLM_AZURE_OPENAI_API_VERSION"]

    def azure_openai_chat_completion_factory(deployment_name: str):
        set_azure() # Langchain bug...
        return AzureChatOpenAI(
            deployment_name=deployment_name,
            openai_api_base=azure_openai_api_base,
            openai_api_version=azure_openai_api_version,
            openai_api_key=azure_openai_api_key,
            client="",
        )

    for deployment_name, deployment in available_deployments["chat_completion"].items():
        model_factory.register_model(f"azure_openai_{deployment_name}",
                                     lambda deployment_name=deployment_name:
                                     azure_openai_chat_completion_factory(deployment_name))

    for deployment_name, deployment in available_deployments["completion"].items():
        model_factory.register_model(f"azure_openai_{deployment_name}",
                                     lambda model=deployment.model, deployment_name=deployment_name:
                                     AzureOpenAI(
                                         model=model,
                                         deployment_name=deployment_name,
                                         openai_api_base=azure_openai_api_base,
                                         openai_api_version=azure_openai_api_version,
                                         openai_api_key=azure_openai_api_key,
                                         client="",
                                     ))
