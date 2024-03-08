from abc import ABC
from typing import Optional

from pydantic import Field

from .schema import Schema


class NonGradedFeedback(Schema, ABC):
    id: Optional[int] = Field(None, example=1)
    title: Optional[str] = Field(None,
                                 description="The title of the feedback that is shown to the student.",
                                 example="File src/pe1/MergeSort.java at line 12")
    description: Optional[str] = Field(None,
                                       description="The detailed feedback description that is shown to the student.",
                                       example="Your solution is correct.")
    meta: dict = Field({}, example={})

    exercise_id: int = Field(example=1)
    submission_id: int = Field(example=1)

    def to_model(self, is_suggestion: bool = False, lms_id: Optional[int] = None):
        return type(self).get_model_class()(**self.dict(), is_suggestion=is_suggestion, lms_id=lms_id)

    class Config:
        orm_mode = True
