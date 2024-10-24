from pydantic import BaseModel, Field
from typing import Union
from athena import config_schema_provider
from llm_core.models import ModelConfigType, DefaultModelConfig, MiniModelConfig
from module_text_llm.prompts.generate_suggestions import (
  system_message as generate_suggestions_system_message, 
  human_message as generate_suggestions_human_message
)
from enum import Enum
from pydantic import root_validator
from abc import ABC, abstractmethod
from module_text_llm.prompts.cot_suggestions import (
  system_message as generate_cot_suggestions_system_message, 
  human_message as generate_cot_suggestions_human_message
)

from module_text_llm.prompts.refined_cot_suggestions import (
  system_message as generate_refined_cot_suggestions_system_message, 
  human_message as generate_refined_cot_suggestions_human_message
)
class GenerateSuggestionsPrompt(BaseModel):
    """\
Features available: **{problem_statement}**, **{example_solution}**, **{grading_instructions}**, **{max_points}**, **{bonus_points}**, **{submission}**

_Note: **{problem_statement}**, **{example_solution}**, or **{grading_instructions}** might be omitted if the input is too long._\
"""
    system_message: str = Field(default=generate_suggestions_system_message,
                                description="Message for priming AI behavior and instructing it what to do.")
    human_message: str = Field(default=generate_suggestions_human_message,
                               description="Message from a human. The input on which the AI is supposed to act.")

class CoTGenerateSuggestionsPrompt(BaseModel):
    """\
Features cit available: **{problem_statement}**, **{example_solution}**, **{grading_instructions}**, **{max_points}**, **{bonus_points}**, **{submission}**

_Note: **{problem_statement}**, **{example_solution}**, or **{grading_instructions}** might be omitted if the input is too long._\
"""
    system_message: str = Field(default=generate_cot_suggestions_system_message,
                                description="Message for priming AI behavior and instructing it what to do.")
    human_message: str = Field(default=generate_cot_suggestions_human_message,
                               description="Message from a human. The input on which the AI is supposed to act.")
    second_system_message: str = Field(default=generate_refined_cot_suggestions_system_message,
                                description="Message for priming AI behavior and instructing it what to do.")
    answer_message: str = Field(default=generate_refined_cot_suggestions_human_message,
                               description="Message from a human. The input on which the AI is supposed to act.")

class ApproachType(str, Enum):
    basic = "BasicApproach"
    chain_of_thought = "ChainOfThought"


class ApproachConfig(BaseModel, ABC):
    max_input_tokens: int = Field(default=3000, description="Maximum number of tokens in the input prompt.")
    model: ModelConfigType = Field(default=DefaultModelConfig())  # type: ignore

    # @abstractmethod
    # def get_prompt(self):
    #     """Abstract method to get the appropriate prompt configuration."""
    #     pass
    
    class Config:
        # Enable discriminator to distinguish between subclasses in the schema
        use_enum_values = True
    
class BasicApproachConfig(ApproachConfig):
    generate_suggestions_prompt: GenerateSuggestionsPrompt = Field(default=GenerateSuggestionsPrompt())

    # def get_prompt(self):
    #     return self.generate_suggestions_prompt

class ChainOfThoughtConfig(ApproachConfig):
    model: ModelConfigType = Field(default=MiniModelConfig)  # type: ignore
    generate_suggestions_prompt: CoTGenerateSuggestionsPrompt = Field(default=CoTGenerateSuggestionsPrompt())

    # def get_prompt(self):
    #     return self.generate_suggestions_prompt
    
# available_approaches = [BasicApproachConfig, ChainOfThoughtConfig]
ApproachConfigUnion = Union[BasicApproachConfig, ChainOfThoughtConfig]

# def approach_factory(approach_type: ApproachType) -> ApproachConfig:
#     if approach_type == ApproachType.basic:
#         return BasicApproachConfig()
#     elif approach_type == ApproachType.chain_of_thought:
#         return ChainOfThoughtConfig()
#     else:
#         raise ValueError(f"Unknown approach type: {approach_type}")
    
@config_schema_provider
class Configuration(BaseModel):
    debug: bool = Field(default=False, description="Enable debug mode.")
    approach: ApproachConfigUnion = Field(default_factory=BasicApproachConfig)  # Default to BasicApproach
    # approach_type: ApproachType = Field(default=ApproachType.basic, description="Type of approach to use.")
    
    # @root_validator(pre=True)
    # def populate_approach(cls, values):
    #     """Automatically instantiate the correct approach based on approach_type."""
    #     approach_type = values.get('approach_type', ApproachType.basic)
    #     values['approach'] = approach_factory(approach_type)
    #     return values
    
