from typing import Callable, Dict, List
from athena import ExerciseTypeVar, Submission, Feedback

FEEDBACK_PROVIDERS: Dict[str, Callable[[ExerciseTypeVar, Submission], List[Feedback]]] = {}


def register_feedback_provider(approach: str):
    def decorator(func: Callable[[ExerciseTypeVar, Submission], List[Feedback]]):
        if approach in FEEDBACK_PROVIDERS:
            raise ValueError(f"Approach '{approach}' is already registered")
        
        FEEDBACK_PROVIDERS[approach] = func
        return func

    return decorator