from typing import Optional
from pydantic import Field

from .feedback import Feedback


class TextFeedback(Feedback):
    """Feedback on a text exercise."""
    index_start: Optional[int] = Field(description="The start index of the feedback in the submission text.", example=0)
    index_end: Optional[int] = Field(description="The end index of the feedback in the submission text.", example=10)

    def __init__(
            self,
            id: Optional[int] = None,
            exercise_id: int = -1,
            submission_id: int = -1,
            detail_text: str = "",
            text: str = "",
            credits: float = 0.0,
            meta: dict = None,  # type: ignore # This is None to avoid mutable default arguments
            index_start: Optional[int] = None,
            index_end: Optional[int] = None,
    ):
        super().__init__(
            id=id,
            exercise_id=exercise_id,
            submission_id=submission_id,
            detail_text=detail_text,
            text=text,
            credits=credits,
            meta=meta,
        )
        self.index_start = index_start
        self.index_end = index_end
