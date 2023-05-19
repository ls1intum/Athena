import inspect
from functools import wraps
from typing import TypeVar, Callable, List, Annotated

from athena.app import app
from athena.logger import logger
from athena.schemas import Exercise, Submission, Feedback
from athena.storage import *

E = TypeVar('E', bound=Exercise)
S = TypeVar('S', bound=Submission)
F = TypeVar('F', bound=Feedback)

def wraps_except_annotations(func: Callable) -> Callable:
    """
    This is a replacement for functools.wraps that ignores annotations.
    This is necessary when the signature of the wrapper function is different from the signature of the wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.__signature__ = inspect.signature(func)
    return wrapper


def submission_selector(func: Callable[[E, List[S]], S]):
    """
    Receive an exercise and some (not necessarily all!) submissions from the Assessment Module Manager and
    return the submission that should ideally be assessed next.
    If the selector returns None, the LMS will select a random submission in the end.
    """
    exercise_type = inspect.signature(func).parameters["exercise"].annotation
    submission_type = inspect.signature(func).parameters["submissions"].annotation.__args__[0]

    @app.post("/select_submission")
    @wraps_except_annotations
    def wrapper(exercise: Annotated[E, exercise_type], submission_ids: List[int]) -> int:
        # The wrapper handles only transmitting submission IDs for efficiency, but the actual selection logic
        # only works with the full submission objects.

        exercise.meta.update(get_stored_exercise_meta(exercise) or {})

        # Get the full submission objects
        submissions = list(get_stored_submissions(submission_type, exercise.id, submission_ids))
        if len(submission_ids) != len(submissions):
            logger.warning("Not all submissions were found in the database! "
                           "Have you sent all submissions to the submission consumer before?")
        if not submissions:
            # Nothing to select from
            return -1

        # Select the submission
        submission = func(exercise, submissions)

        # Store exercise and submissions with potentially changed metadata
        store_exercise(exercise)
        store_submissions(submissions)

        if submission is None:
            return -1
        return submission.id

    return wrapper


def submissions_consumer(func: Callable[[E, List[S]], None]):
    """
    Receive submissions from the Assessment Module Manager and automatically store them in the database.
    The submissions consumer is usually called whenever the deadline for an exercise is reached.
    """

    @app.post("/submissions")
    @wraps(func)
    def wrapper(exercise, submissions):
        # Retrieve existing metadata for the exercise and submissions
        exercise.meta.update(get_stored_exercise_meta(exercise) or {})
        submissions_dict = {s.id: s for s in submissions}
        if submissions:
            stored_submissions = get_stored_submissions(submissions[0].__class__, exercise.id, [s.id for s in submissions])
            for stored_submission in stored_submissions:
                if stored_submission.id in submissions_dict:
                    submissions_dict[stored_submission.id].meta.update(stored_submission.meta)
        submissions = list(submissions_dict.values())

        # Call the actual consumer
        func(exercise, submissions)

        # Store exercise and submissions (with potentially changed metadata)
        store_exercise(exercise)
        store_submissions(submissions)

    return wrapper


def feedback_consumer(func: Callable[[E, S, F], None]):
    """
    Receive feedback from the Assessment Module Manager and automatically store it in the database.
    The feedback consumer is usually called whenever the LMS gets feedback from a tutor.
    """

    @app.post("/feedback")
    @wraps(func)
    def wrapper(exercise, submission, feedback):
        # Retrieve existing metadata for the exercise, submission and feedback
        exercise.meta.update(get_stored_exercise_meta(exercise) or {})
        submission.meta.update(get_stored_submission_meta(submission) or {})
        feedback.meta.update(get_stored_feedback_meta(feedback) or {})

        # Call the actual consumer
        func(exercise, submission, feedback)

        # Store feedback, exercise, and submission with potentially changed metadata
        store_feedback(feedback)
        store_exercise(exercise)
        store_submissions([submission])

    return wrapper


def feedback_provider(func: Callable[[E, S], List[F]]):
    """
    Provide feedback to the Assessment Module Manager.
    The feedback provider is usually called whenever the tutor requests feedback for a submission in the LMS.
    """
    @app.post("/feedback_suggestions")
    @wraps(func)
    def wrapper(exercise, submission):
        # Retrieve existing metadata for the exercise, submission and feedback
        exercise.meta.update(get_stored_exercise_meta(exercise) or {})
        submission.meta.update(get_stored_submission_meta(submission) or {})

        # Call the actual provider
        feedbacks = func(exercise, submission)

        # Store exercise and submission potentially changed metadata
        store_feedback_suggestions(feedbacks)
        store_exercise(exercise)
        store_submissions([submission])

        return feedbacks
    return wrapper
