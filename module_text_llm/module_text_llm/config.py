from abc import ABC, abstractproperty
from pydantic import BaseModel, Field
from module_text_llm.helpers.models import model_config
from .prompts.suggest_feedback_basic import system_template, human_template


basic_features = [
    "problem_statement",
    "grading_instructions",
    "submission",
    "max_points",
    "bonus_points",
]


class Prompt(BaseModel):
    system_message: str
    human_message: str


class BasicPrompt(Prompt):
    """Features available:
    {problem_statement}, {grading_instructions}, {submission}, {max_points}, {bonus_points}
    """
    system_message: str = Field(default=system_template, 
                                description="A Message for priming AI behavior, usually passed in as the first of a sequence of input messages.")
    human_message: str = Field(default=human_template, 
                               description="A Message from a human. Usually the input on which the AI is supposed to act.")


class BasicApproach(BaseModel):
    """Basic approach.

    This approach uses a LLM with a single prompt to generate feedback in a single step.
    """
    model: model_config
    prompt: BasicPrompt


class Configuration(BaseModel):
    approach: BasicApproach
    # model: model_config





# class ApprochesType(str, Enum):
#     BASIC = "basic"
#     BASIC_FINETUNED = "basic_finetuned"
#     ADVANCED = "advanced"


# class ModelConfig(BaseModel, ABC):
#     pass


# class OpenAILLMConfig(ModelConfig):




# # Abstract ABC
# class CommonApproachConfig(BaseModel, ABC):
#     @abstractproperty
#     def name(self) -> str:
#         pass

#     # ModelConfig
#     model:
    
    

    



# class ModelOption(BaseModel):
#     temperature: float = Field(..., ge=0, le=1,
#                                description="The temperature to use for the model")
#     top_k: int = Field(..., ge=0,
#                        description="The number of top-k options to consider")
#     top_p: float = Field(..., ge=0, le=1,
#                          description="The number of top-p options to consider")


# class Model(BaseModel):
#     name: str = Field(..., description="The name of the model")
#     options: ModelOption = Field(..., description="The options for the model")


# class Approach(BaseModel):
#     name: str = Field(..., description="The name of the approach")
#     models: List[Model] = Field(...,
#                                 description="The list of models for the approach")
#     predefined_prompts: Dict[str, str] = Field(
#         ..., description="The dictionary of predefined prompts for the approach")


# class ConfigOptions(BaseModel):
#     approaches: List[Approach] = Field(..., description="The list of approaches")





# config = ConfigOptions(
#     approaches=[
#         Approach(
#             name="basic",
#             models=[
#                 Model(name="gpt4", options=ModelOption(
#                     temperature=0.6, top_k=50, top_p=0.9)),
#                 Model(name="gpt3", options=ModelOption(
#                     temperature=0.7, top_k=40, top_p=0.8)),
#             ],
#             predefined_prompts={
#                 "prompt1": "Tell me a joke",
#                 "prompt2": "Tell me a story",
#             }
#         ),
#         Approach(
#             name="finetuned",
#             models=[
#                 Model(name="gpt4_finetuned", options=ModelOption(
#                     temperature=0.6, top_k=50, top_p=0.9)),
#                 Model(name="gpt3_finetuned", options=ModelOption(
#                     temperature=0.7, top_k=40, top_p=0.8)),
#             ],
#             predefined_prompts={
#                 "prompt1": "Tell me a joke",
#                 "prompt2": "Tell me a story",
#             }
#         ),
#     ]
# )
