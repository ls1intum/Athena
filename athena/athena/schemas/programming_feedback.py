from typing import Optional, Tuple

from pydantic import BaseModel, Field

from .feedback import Feedback


class ProgrammingFeedback(Feedback, BaseModel):
    """Feedback on a programming exercise."""
    file_path: Optional[str] = Field(None, example="src/pe1/MergeSort.java")
    line_start: Optional[int] = Field(None, example=1)
    line_end: Optional[int] = Field(None, example=2)

    @property
    def line_range(self) -> Tuple[int, int]:
        """Return the line range of this feedback, even if it is only a single line (line_end is None)."""
        if self.line_start is None:
            raise ValueError("Feedback does not have a line start")
        if self.line_end is None:
            return (self.line_start, self.line_start)
        return (self.line_start, self.line_end)
