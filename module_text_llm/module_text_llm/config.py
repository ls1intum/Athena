from pydantic import BaseModel
from module_text_llm.helpers.models import model_config


class Configuration(BaseModel):
    model: model_config



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
