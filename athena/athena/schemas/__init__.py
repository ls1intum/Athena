"""Schemas are pydantic models for data transfer objects (DTOs)."""

from .exercise_type import ExerciseType
from .exercise import Exercise
from .feedback import GradedFeedback
from .submission import Submission
from .text_exercise import TextExercise
from .text_submission import TextSubmission, TextLanguageEnum
from .feedback import GradedProgrammingFeedback
from .programming_exercise import ProgrammingExercise
from .programming_submission import ProgrammingSubmission
from .modelling_exercise import ModellingExercise
from .modelling_submission import ModellingSubmission
from .grading_criterion import GradingCriterion, StructuredGradingInstruction
from .feedback import NonGradedFeedback
from .feedback import NonGradedProgrammingFeedback
from .feedback import GradedModellingFeedback
from .feedback import GradedTextFeedback
from .feedback import Feedback