from pydantic import BaseModel, Field
from module_text_llm.helpers.models import model_config, default_model_config
from .prompts.suggest_feedback_basic import system_template, human_template


class Prompt(BaseModel):
    system_message: str
    human_message: str


class BasicPrompt(Prompt):
    """Features available: **{problem_statement}**, **{grading_instructions}**, **{submission}**, **{max_points}**, **{bonus_points}**
    """
    system_message: str = Field(default=system_template,
                                description="A Message for priming AI behavior, usually passed in as the first of a sequence of input messages.")
    human_message: str = Field(default=human_template,
                               description="A Message from a human. Usually the input on which the AI is supposed to act.")


class BasicApproachConfig(BaseModel):
    """Basic approach.

    This approach uses a LLM with a single prompt to generate feedback in a single step.
    """
    model: model_config
    prompt: BasicPrompt


class Configuration(BaseModel):
    debug: bool = Field(default=False, description="Enable debug mode.")
    approach: BasicApproachConfig


default_config = Configuration(
    approach=BasicApproachConfig(
        model=default_model_config,
        prompt=BasicPrompt(
            system_message=system_template,
            human_message=human_template
        )
    )
)
