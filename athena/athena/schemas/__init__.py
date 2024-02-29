"""Schemas are pydantic models for data transfer objects (DTOs)."""

from .exercise_type import ExerciseType
from .exercise import Exercise
from .graded_feedback import GradedFeedback
from .submission import Submission
from .graded_text_feedback import TextGradedFeedback
from .text_exercise import TextExercise
from .text_submission import TextSubmission, TextLanguageEnum
from .graded_programming_feedback import ProgrammingGradedFeedback
from .programming_exercise import ProgrammingExercise
from .programming_submission import ProgrammingSubmission
from .graded_modelling_feedback import ModellingGradedFeedback
from .modelling_exercise import ModellingExercise
from .modelling_submission import ModellingSubmission
from .grading_criterion import GradingCriterion, StructuredGradingInstruction