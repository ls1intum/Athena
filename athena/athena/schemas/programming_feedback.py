from typing import Optional, Tuple

from pydantic import Field

from .feedback import Feedback


class ProgrammingFeedback(Feedback):
    """Feedback on a programming exercise."""
    file_path: Optional[str] = Field(None, example="src/pe1/MergeSort.java")
    line_start: Optional[int] = Field(None, example=1)
    line_end: Optional[int] = Field(None, example=2)

    def __init__(
            self,
            id: Optional[int] = None,
            exercise_id: int = -1,
            submission_id: int = -1,
            detail_text: str = "",
            text: str = "",
            credits: float = 0.0,
            meta: dict = None,  # type: ignore # This is None to avoid mutable default arguments
            file_path: Optional[str] = None,
            line_start: Optional[int] = None,
            line_end: Optional[int] = None,
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
        self.file_path = file_path
        self.line_start = line_start
        self.line_end = line_end


    @property
    def line_range(self) -> Tuple[int, int]:
        """Return the line range of this feedback, even if it is only a single line (line_end is None)."""
        if self.line_start is None:
            raise ValueError("Feedback does not have a line start")
        if self.line_end is None:
            return (self.line_start, self.line_start)
        return (self.line_start, self.line_end)
