from pydantic import BaseModel, Field
from typing import Union
from athena import config_schema_provider

from module_text_llm.approaches.chain_of_thought_approach.config import ChainOfThoughtConfig
from module_text_llm.approaches.basic_approach.config import BasicApproachConfig

ApproachConfigUnion = Union[ChainOfThoughtConfig, BasicApproachConfig]

@config_schema_provider
class Configuration(BaseModel):
    debug: bool = Field(default=False, description="Enable debug mode.")
    approach: ApproachConfigUnion = Field(default_factory=BasicApproachConfig)  # Default to BasicApproach

    class Config:
        smart_union = True 
