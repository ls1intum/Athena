from abc import ABC
from typing import Optional

from pydantic import Field

from .schema import Schema


class Feedback(Schema, ABC):
    id: Optional[int] = Field(None, example=1)
    exercise_id: int = Field(example=1)
    submission_id: int = Field(example=1)
    detail_text: str = Field(description="The detailed feedback text that is shown to the student.",
                             example="Your solution is correct.")
    text: str = Field(description="The title of the feedback that is shown to the student.",
                      example="File src/pe1/MergeSort.java at line 12")
    credits: float = Field(description="The number of points that the student received for this feedback.",
                           example=1.0)

    meta: dict = Field(example={})

    def to_model(self, is_suggestion: bool = False):
        return type(self).get_model_class()(**self.dict(), is_suggestion=is_suggestion)

    class Config:
        orm_mode = True
