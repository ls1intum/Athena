from typing import Callable
from langchain.base_language import BaseLanguageModel
from athena.logger import logger


class LanguageModelFactory:
    def __init__(self):
        self.model_builders: dict[str, Callable[..., BaseLanguageModel]] = {}

    def register_model(self, model_key: str, builder: Callable[..., BaseLanguageModel]): 
        self.model_builders[model_key] = builder

    def create(self, model_key: str) -> BaseLanguageModel:
        builder = self.model_builders.get(model_key)
        if not builder:
            raise ValueError(model_key)
        return builder()


model_factory = LanguageModelFactory()