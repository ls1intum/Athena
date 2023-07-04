import os 
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.llms.openai import AzureOpenAI
from langchain.llms.loading import load_llm_from_config
import openai

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


# Validate environment variables
if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")
if OPENAI_API_TYPE == "azure":
    if "OPENAI_API_BASE" not in os.environ:
        raise EnvironmentError("OPENAI_API_TYPE=azure but OPENAI_API_BASE environment variable not set.")
    if "OPENAI_API_VERSION" not in os.environ:
        raise EnvironmentError("OPENAI_API_TYPE=azure but OPENAI_API_VERSION environment variable not set.")
    if "AZURE_DEPLOYMENT_NAME" not in os.environ:
        raise EnvironmentError("OPENAI_API_TYPE=azure but AZURE_DEPLOYMENT_NAME environment variable not set.")
    
    AZURE_DEPLOYMENT_NAME = os.environ["AZURE_DEPLOYMENT_NAME"]
 
    # Check if deployment exists
    openai.api_type = "azure"
    key = os.environ["OPENAI_API_KEY"]
    openai.api_key = key
    openai.api_base = os.environ["OPENAI_API_BASE"]
    openai.api_version = os.environ["OPENAI_API_VERSION"]
     
    deployments[key] = openai.Deployment.list().data # type: ignore
    deployment_ids = [deployment.id for deployment in deployments[key]]
    if AZURE_DEPLOYMENT_NAME not in deployment_ids:
        deployments_list = [{ "id": deployment.id, "model": deployment.model } for deployment in deployments[key]]
        raise EnvironmentError(f"Deployment id '{AZURE_DEPLOYMENT_NAME}' not found, available deployments: {deployments_list}")

    # Initialize azure chat model
    chat = AzureChatOpenAI(deployment_name=AZURE_DEPLOYMENT_NAME, client="", temperature=0)
else:
    # Initialize openai chat model
    chat = ChatOpenAI(client="", temperature=0)


def get_azure_model_cls(api_key, api_base, api_version, deployment_name):
    global deployments

    # Some caching of the deployments requests
    if api_key not in deployments:
        openai.api_type = "azure"
        openai.api_key = api_key
        openai.api_base = api_base
        openai.api_version = api_version
        deployments[api_key] = openai.Deployment.list().data # type: ignore

    deployment_ids = [deployment.id for deployment in deployments[api_key]]
    if deployment_name not in deployment_ids:
        deployments_list = [{ "id": deployment.id, "model": deployment.model } for deployment in deployments[api_key]]
        raise EnvironmentError(f"Deployment id '{deployment_name}' not found, available deployments: {deployments_list}")
    
    model_name = [deployment.model for deployment in deployments[api_key] if deployment.id == deployment_name][0]
    if model_name not in chatModels:
        return AzureChatOpenAI
    else:
        return AzureOpenAI


def get_model_from_exercise_meta(exercise: Exercise):
    if "llm_model_config" not in exercise.meta:
        return None
    config = exercise.meta["llm_model_config"].copy()
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
        return load_llm_from_config(config)