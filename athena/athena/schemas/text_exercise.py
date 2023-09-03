from typing import Optional
from pydantic import Field

from .exercise_type import ExerciseType
from .exercise import Exercise


class TextExercise(Exercise):
    """A text exercise that can be solved by students, enhanced with metadata."""

    type: ExerciseType = Field(ExerciseType.text, const=True)

    example_solution: Optional[str] = Field(None, description="An example solution to the exercise.")
