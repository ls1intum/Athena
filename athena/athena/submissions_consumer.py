"""
This module provides a decorator for submission consumers.
"""
from functools import wraps
from typing import List, Callable

from .app import app
from .models import Exercise, Submission
from .storage import store_submission


def submissions_consumer(func: Callable[[Exercise, List[Submission]], None]):
    """
    Receive submissions from the Assessment Module Manager and automatically store them in the database.
    The submissions consumer is usually called whenever the deadline for an exercise is reached.
    """
    @app.post("/submissions")
    @wraps(func)
    def wrapper(exercise: Exercise, submissions: List[Submission]):
        for submission in submissions:
            store_submission(submission)
        return func(exercise, submissions)

    return wrapper
