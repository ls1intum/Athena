from abc import ABC
from pydantic import BaseModel, Field
from llm_core.models import ModelConfigType, DefaultModelConfig, MiniModelConfig

class ApproachConfig(BaseModel, ABC):
    max_input_tokens: int = Field(default=3000, description="Maximum number of tokens in the input prompt.")
    model: ModelConfigType = Field(default=DefaultModelConfig())  # type: ignore
    
    class Config:
        use_enum_values = True