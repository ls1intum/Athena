"""Import this to use schemas and decorators specific to programming exercises."""
import functools

import athena.storage
from .module_config import get_module_config
from .schemas import ProgrammingExercise, GradedProgrammingFeedback, ProgrammingSubmission, NonGradedProgrammingFeedback

module_type = get_module_config().type
if module_type.name != "programming":
    raise ImportError(f"Importing athena.programming from a module of type {module_type}. This is probably a mistake, "
                      f"you should only import the file related to the exercise type that your module handles")

# re-export with shorter names, because the module will only use these
Exercise = ProgrammingExercise
Submission = ProgrammingSubmission
GradedFeedback = GradedProgrammingFeedback
NonGradedFeedback = NonGradedProgrammingFeedback

# re-export without the need to give the type of the requested schema
get_stored_exercises = functools.partial(athena.storage.get_stored_exercises, Exercise)
count_stored_submissions = functools.partial(athena.storage.count_stored_submissions, Submission)
get_stored_submissions = functools.partial(athena.storage.get_stored_submissions, Submission)
get_stored_feedback = functools.partial(athena.storage.get_stored_feedback, GradedFeedback)
get_stored_feedback_suggestions = functools.partial(athena.storage.get_stored_feedback_suggestions, GradedFeedback)

__all__ = [
    "Exercise", "Submission", "GradedFeedback",
    "get_stored_exercises", "get_stored_submissions", "get_stored_feedback", "get_stored_feedback_suggestions"
]
