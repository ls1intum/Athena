from typing import Optional
from pydantic import Field

from .feedback import Feedback


class TextFeedback(Feedback):
    """Feedback on a text exercise."""
    index_start: Optional[int] = Field(None, description="The start index of the feedback in the submission text.", example=0)
    index_end: Optional[int] = Field(None, description="The end index of the feedback in the submission text.", example=10)
