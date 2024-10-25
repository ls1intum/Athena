from pydantic import BaseModel, Field
from typing import Literal
from llm_core.models import ModelConfigType, MiniModelConfig

from module_text_llm.approaches.chain_of_thought_approach.prompts.cot_suggestions import (
  system_message as generate_cot_suggestions_system_message, 
  human_message as generate_cot_suggestions_human_message
)

from module_text_llm.approaches.chain_of_thought_approach.prompts.refined_cot_suggestions import (
  system_message as generate_refined_cot_suggestions_system_message, 
  human_message as generate_refined_cot_suggestions_human_message
)

from module_text_llm.approaches.approach_config import ApproachConfig

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

class ChainOfThoughtConfig(ApproachConfig):
    # Defaults to the cheaper mini 4o model
    type: Literal['chain_of_thought'] = 'chain_of_thought'
    model: ModelConfigType = Field(default=MiniModelConfig)  # type: ignore
    generate_suggestions_prompt: CoTGenerateSuggestionsPrompt = Field(default=CoTGenerateSuggestionsPrompt())
