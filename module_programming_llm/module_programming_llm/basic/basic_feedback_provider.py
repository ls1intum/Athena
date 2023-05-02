from typing import List

from athena import Feedback, ProgrammingExercise, Submission

from ..feedback_provider_registry import register_feedback_provider


@register_feedback_provider("basic")
def suggest_feedback(exercise: ProgrammingExercise, submission: Submission) -> List[Feedback]:
    # Your basic feedback provider implementation
    print("basic")
    return []