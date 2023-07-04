import os
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.llms.openai import AzureOpenAI
from langchain.llms.loading import load_llm_from_config
import openai

from athena.logger import logger
from athena.text import Exercise


OPENAI_API_TYPE = os.environ.get("OPENAI_API_TYPE")

# api_keys -> deplyments
deployments = {}

# https://platform.openai.com/docs/models/model-endpoint-compatibility
# /v1/chat/completions	gpt-4, gpt-4-0613, gpt-4-32k, gpt-4-32k-0613, gpt-3.5-turbo, gpt-3.5-turbo-0613, gpt-3.5-turbo-16k, gpt-3.5-turbo-16k-0613
# /v1/completions	text-davinci-003, text-davinci-002, text-curie-001, text-babbage-001, text-ada-001
# We have to keep it manually in sync with the OpenAI API for now

chatModels = [
    "gpt-4",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0613",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
]

textModels = [
    "text-davinci-003",
    "text-davinci-002",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
]


def get_azure_model_cls(api_key, api_base, api_version, deployment_name):
    global deployments

    # Some caching of the deployments requests
    if api_key not in deployments:
        openai.api_type = "azure"
        openai.api_key = api_key
        openai.api_base = api_base
        openai.api_version = api_version

        deployments[api_key] = openai.Deployment.list().data  # type: ignore

    deployment_ids = [deployment.id for deployment in deployments[api_key]]
    if deployment_name not in deployment_ids:
        deployments_list = [{"id": deployment.id, "model": deployment.model}
                            for deployment in deployments[api_key]]
        raise EnvironmentError(
            f"Deployment id '{deployment_name}' not found, available deployments: {deployments_list}")

    model_name = [deployment.model for deployment in deployments[api_key]
                  if deployment.id == deployment_name][0]
    if model_name not in chatModels:
        return AzureChatOpenAI
    else:
        return AzureOpenAI


# Validate environment variables
if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")
if OPENAI_API_TYPE == "azure":
    if "OPENAI_API_BASE" not in os.environ:
        raise EnvironmentError(
            "OPENAI_API_TYPE=azure but OPENAI_API_BASE environment variable not set.")
    if "OPENAI_API_VERSION" not in os.environ:
        raise EnvironmentError(
            "OPENAI_API_TYPE=azure but OPENAI_API_VERSION environment variable not set.")
    if "AZURE_DEPLOYMENT_NAME" not in os.environ:
        raise EnvironmentError(
            "OPENAI_API_TYPE=azure but AZURE_DEPLOYMENT_NAME environment variable not set.")

    AZURE_DEPLOYMENT_NAME = os.environ["AZURE_DEPLOYMENT_NAME"]

    Model = get_azure_model_cls(
        api_key=os.environ["OPENAI_API_KEY"],
        api_base=os.environ["OPENAI_API_BASE"],
        api_version=os.environ["OPENAI_API_VERSION"],
        deployment_name=os.environ["AZURE_DEPLOYMENT_NAME"]
    )

    default_model = Model(deployment_name=AZURE_DEPLOYMENT_NAME,
                          client="", temperature=0)  # type: ignore
else:
    # Initialize openai chat model
    default_model = ChatOpenAI(client="", temperature=0)


def get_model_from_exercise_meta(exercise: Exercise):
    if "llm_model_config" not in exercise.meta:
        return None

    config = exercise.meta["llm_model_config"].copy()
    logger.info(f"Loading model from exercise meta: {config}")
    if config.get("_type") == "azure":
        del config["_type"]
        Model = get_azure_model_cls(
            api_key=config["openai_api_key"],
            api_base=config["openai_api_base"],
            api_version=config["openai_api_version"],
            deployment_name=config["deployment_name"]
        )
        return Model(**config)
    else:
        # openai.api_type = "open_ai"
        # openai.api_version = None
        # openai.api_base = "https://api.openai.com/v1"
        # openai.api_key = config["openai_api_key"]
        logger.info(config["openai_api_key"])
        # No longer supported by load_llm_from_config
        if config["model_name"] in chatModels:
            del config["_type"]
            return ChatOpenAI(**config)
        return load_llm_from_config(config)
