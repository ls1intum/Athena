from module_text_llm.approaches.approach_config import ApproachConfig
from pydantic import Field, BaseModel
from typing import Literal


from module_text_llm.approaches.basic_approach.prompts.generate_suggestions import (
  system_message as generate_suggestions_system_message, 
  human_message as generate_suggestions_human_message
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

    
class BasicApproachConfig(ApproachConfig):
    type: Literal['basic'] = 'basic'
    generate_suggestions_prompt: GenerateSuggestionsPrompt = Field(default=GenerateSuggestionsPrompt())

