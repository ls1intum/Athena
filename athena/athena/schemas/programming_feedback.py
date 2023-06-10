from typing import Optional

from pydantic import Field

from .feedback import Feedback


class ProgrammingFeedback(Feedback):
    """Feedback on a programming exercise."""
    file_path: Optional[str] = Field(None, example="src/pe1/MergeSort.java")
    line_start: Optional[int] = Field(None, example=1)
    line_end: Optional[int] = Field(None, example=2)
