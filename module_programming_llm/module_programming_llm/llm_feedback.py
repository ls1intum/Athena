from pydantic import BaseModel, Field
from typing import List, Optional

class LLMFeedback(BaseModel):
    text: str = Field(description="comment to the student")
    line: Optional[int] = Field(description="optional line number to comment on")
    credits: int = Field(description="credits to award or deduct from the student's submission")

class ListLLMFeedback(BaseModel):
	feedback: List[LLMFeedback] = Field(description="list of feedback items")