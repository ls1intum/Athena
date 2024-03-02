from typing import Optional

from pydantic import Field

from athena.schemas.feedback.feedback import Feedback


class GradedFeedback(Feedback):
    credits: float = Field(0.0,
                           description="The number of points that the student received for this feedback.",
                           example=1.0)
    structured_grading_instruction_id: Optional[int] = Field(None,
                                                             description="The id of the structured grading instruction that this feedback belongs to.",
                                                             example=1)

    def to_model(self, is_suggestion: bool = False, lms_id: Optional[int] = None):
        return type(self).get_model_class()(**self.dict(), is_suggestion=is_suggestion, lms_id=lms_id)