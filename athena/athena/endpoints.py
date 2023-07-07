# type: ignore # too much weird behavior of mypy with decorators
import inspect
from typing import TypeVar, Callable, List, Union, Any, Coroutine

from pydantic import BaseModel

from athena.app import app
from athena.authenticate import authenticated
from athena.logger import logger
from athena.schemas import Exercise, Submission, Feedback
from athena.schemas.schema import to_camel
from athena.storage import get_stored_submission_meta, get_stored_exercise_meta, get_stored_feedback_meta, \
    store_exercise, store_feedback, store_feedback_suggestions, store_submissions, get_stored_submissions
    

E = TypeVar('E', bound=Exercise)
S = TypeVar('S', bound=Submission)
F = TypeVar('F', bound=Feedback)


module_responses = {
    403: {
        "description": "API secret is invalid - set the environment variable SECRET and the Authorization header "
                       "to the same value",
    }
}


def submissions_consumer(func: Union[Callable[[E, List[S]], None], Callable[[E, List[S]], Coroutine[Any, Any, None]]]):
    """
    Receive submissions from the Assessment Module Manager.
    The submissions consumer is usually called whenever the deadline for an exercise is reached.
    """
    exercise_type = inspect.signature(func).parameters["exercise"].annotation
    submission_type = inspect.signature(func).parameters["submissions"].annotation.__args__[0]

    @app.post("/submissions", responses=module_responses)
    @authenticated
    async def wrapper(
            exercise: exercise_type,
            submissions: List[submission_type]):
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
        if inspect.iscoroutinefunction(func):
            await func(exercise, submissions)
        else:
            func(exercise, submissions)

    return wrapper


def submission_selector(func: Union[Callable[[E, List[S]], S], Callable[[E, List[S]], Coroutine[Any, Any, S]]]):
    """
    Receive an exercise and some (not necessarily all!) submissions from the Assessment Module Manager and
    return the submission that should ideally be assessed next.
    If the selector returns None, the LMS will select a random submission in the end.
    """
    exercise_type = inspect.signature(func).parameters["exercise"].annotation
    submission_type = inspect.signature(func).parameters["submissions"].annotation.__args__[0]

    # own request model to allow for `submissionIds` instead of `submission_ids` (camelCase vs snake_case)
    class SubmissionSelectorRequest(BaseModel):
        exercise: exercise_type
        submission_ids: List[int]
    
        class Config:
            # Allow camelCase field names in the API (converted to snake_case)
            alias_generator = to_camel
            allow_population_by_field_name = True

    @app.post("/select_submission", responses=module_responses)
    @authenticated
    async def wrapper(req: SubmissionSelectorRequest) -> int:
        exercise = req.exercise
        submission_ids = req.submission_ids
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
        if inspect.iscoroutinefunction(func):
            submission = await func(exercise, submissions)
        else:
            submission = func(exercise, submissions)

        if submission is None:
            return -1
        return submission.id

    return wrapper


def feedbacks_consumer(func: Union[Callable[[E, S, List[F]], None], Callable[[E, S, List[F]], Coroutine[Any, Any, None]]]):
    """
    Receive feedback from the Assessment Module Manager.
    The feedback consumer is usually called whenever the LMS gets feedback from a tutor.
    """
    exercise_type = inspect.signature(func).parameters["exercise"].annotation
    submission_type = inspect.signature(func).parameters["submission"].annotation
    feedbacks_type = inspect.signature(func).parameters["feedbacks"].annotation

    @app.post("/feedbacks", responses=module_responses)
    @authenticated
    async def wrapper(
            exercise: exercise_type,
            submission: submission_type,
            feedbacks: feedbacks_type):
        # Retrieve existing metadata for the exercise, submission and feedback
        exercise.meta.update(get_stored_exercise_meta(exercise) or {})
        submission.meta.update(get_stored_submission_meta(submission) or {})
        for feedback in feedbacks:
            feedback.meta.update(get_stored_feedback_meta(feedback) or {})
            store_feedback(feedback)

        # Call the actual consumer
        if inspect.iscoroutinefunction(func):
            await func(exercise, submission, feedbacks)
        else:
            func(exercise, submission, feedbacks)

    return wrapper


def feedback_provider(func: Union[Callable[[E, S], List[F]], Callable[[E, S], Coroutine[Any, Any, List[F]]]]):
    """
    Provide feedback to the Assessment Module Manager.
    The feedback provider is usually called whenever the tutor requests feedback for a submission in the LMS.
    """
    exercise_type = inspect.signature(func).parameters["exercise"].annotation
    submission_type = inspect.signature(func).parameters["submission"].annotation

    @app.post("/feedback_suggestions", responses=module_responses)
    @authenticated
    async def wrapper(
            exercise: exercise_type,
            submission: submission_type):
        # Retrieve existing metadata for the exercise, submission and feedback
        exercise.meta.update(get_stored_exercise_meta(exercise) or {})
        submission.meta.update(get_stored_submission_meta(submission) or {})

        store_exercise(exercise)
        store_submissions([submission])

        # Call the actual provider
        if inspect.iscoroutinefunction(func):
            feedbacks = await func(exercise, submission)
        else:
            feedbacks = func(exercise, submission)
    
        store_feedback_suggestions(feedbacks)

        return feedbacks
    return wrapper
