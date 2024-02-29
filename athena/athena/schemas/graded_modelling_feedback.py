from typing import Optional, List

from pydantic import Field

from .graded_feedback import GradedFeedback


class ModellingGradedFeedback(GradedFeedback):
    """Feedback on a modelling exercise."""

    element_ids: Optional[List[str]] = Field([], description="referenced diagram element IDs", example=["id_1"])
