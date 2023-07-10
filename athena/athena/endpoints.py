# type: ignore # too much weird behavior of mypy with decorators
import inspect
import json
from fastapi import Header, Depends
from pydantic import BaseModel
from typing import TypeVar, Callable, List, Dict, Union, Any, Coroutine, Optional

from athena import get_meta
from athena.app import app
from athena.authenticate import authenticated
from athena.logger import logger
from athena.schemas import Exercise, Submission, Feedback
from athena.storage import get_stored_submission_meta, get_stored_exercise_meta, get_stored_feedback_meta, \
    store_exercise, store_feedback, store_feedback_suggestions, store_submissions, get_stored_submissions


E = TypeVar('E', bound=Exercise)
S = TypeVar('S', bound=Submission)
F = TypeVar('F', bound=Feedback)


module_responses = {
    403: {
        "description": "API secret is invalid - set the environment variable SECRET and the X-API-Secret header "
                       "to the same value",
    }
}


def submissions_consumer(func: Union[
    Callable[[E, List[S]], None],
    Callable[[E, List[S], Optional[dict]], None],
    Callable[[E, List[S]], Coroutine[Any, Any, None]],
    Callable[[E, List[S], Optional[dict]], Coroutine[Any, Any, None]]
]):
    """
    Receive submissions from the Assessment Module Manager.
    The submissions consumer is usually called whenever the deadline for an exercise is reached.
    """
    exercise_type = inspect.signature(func).parameters["exercise"].annotation
    submission_type = inspect.signature(
        func).parameters["submissions"].annotation.__args__[0]

    @app.post("/submissions", responses=module_responses)
    @authenticated
    async def wrapper(
            exercise: exercise_type,
            submissions: List[submission_type],
            module_config: Optional[str] = Header(
                None, alias="X-Module-Config"),
            metadata: Dict[str, Any] = Depends(get_meta)):
        if module_config:
            try:
                module_config = json.loads(module_config)
            except json.JSONDecodeError:
                logger.warning(
                    "Invalid module config received: %s", module_config)
                module_config = None

        # Retrieve existing metadata for the exercise and submissions
        meta = get_stored_exercise_meta(exercise) or {}
        meta.update(exercise.meta)
        exercise.meta = meta
        submissions_dict = {s.id: s for s in submissions}
        if submissions:
            stored_submissions = get_stored_submissions(
                submissions[0].__class__, exercise.id, [s.id for s in submissions])
            for stored_submission in stored_submissions:
                if stored_submission.id in submissions_dict:
                    meta = get_stored_submission_meta(stored_submission) or {}
                    meta.update(stored_submission.meta)
                    submissions_dict[stored_submission.id].meta = meta
        submissions = list(submissions_dict.values())

        store_exercise(exercise)
        store_submissions(submissions)

        args = [exercise, submissions]
        if len(inspect.signature(func).parameters) > 2:
            args.append(module_config)

        # Call the actual consumer
        if inspect.iscoroutinefunction(func):
            await func(*args)
        else:
            func(*args)

        return {"data": None, "meta": metadata}
    return wrapper


def submission_selector(func: Union[
    Callable[[E, List[S]], S],
    Callable[[E, List[S], Optional[dict]], S],
    Callable[[E, List[S]], Coroutine[Any, Any, S]],
    Callable[[E, List[S], Optional[dict]], Coroutine[Any, Any, S]]
]):
    """
    Receive an exercise and some (not necessarily all!) submissions from the Assessment Module Manager and
    return the submission that should ideally be assessed next.
    If the selector returns None, the LMS will select a random submission in the end.
    """
    exercise_type = inspect.signature(func).parameters["exercise"].annotation
    submission_type = inspect.signature(
        func).parameters["submissions"].annotation.__args__[0]

    @app.post("/select_submission", responses=module_responses)
    @authenticated
    async def wrapper(
            exercise: exercise_type,
            submission_ids: List[int],
            module_config: Optional[str] = Header(
                None, alias="X-Module-Config"),
            metadata: Dict[str, Any] = Depends(get_meta)):
        # The wrapper handles only transmitting submission IDs for efficiency, but the actual selection logic
        # only works with the full submission objects.

        if module_config:
            try:
                module_config = json.loads(module_config)
            except json.JSONDecodeError:
                logger.warning(
                    "Invalid module config received: %s", module_config)
                module_config = None

        exercise.meta.update(get_stored_exercise_meta(exercise) or {})

        # Get the full submission objects
        submissions = list(get_stored_submissions(
            submission_type, exercise.id, submission_ids))
        if len(submission_ids) != len(submissions):
            logger.warning("Not all submissions were found in the database! "
                           "Have you sent all submissions to the submission consumer before?")
        if not submissions:
            # Nothing to select from
            return {"data": -1, "meta": metadata}

        args = [exercise, submissions]
        if len(inspect.signature(func).parameters) > 2:
            args.append(module_config)

        # Select the submission
        if inspect.iscoroutinefunction(func):
            submission = await func(*args)
        else:
            submission = func(*args)

        if submission is None:
            return {"data": -1, "meta": metadata}
        return {"data": submission.id, "meta": metadata}

    return wrapper


def feedback_consumer(func: Union[
    Callable[[E, S, F], None],
    Callable[[E, S, F, Optional[dict]], None],
    Callable[[E, S, F], Coroutine[Any, Any, None]],
    Callable[[E, S, F, Optional[dict]], Coroutine[Any, Any, None]]
]):
    """
    Receive feedback from the Assessment Module Manager.
    The feedback consumer is usually called whenever the LMS gets feedback from a tutor.
    """
    exercise_type = inspect.signature(func).parameters["exercise"].annotation
    submission_type = inspect.signature(
        func).parameters["submission"].annotation
    feedback_type = inspect.signature(func).parameters["feedback"].annotation

    @app.post("/feedback", responses=module_responses)
    @authenticated
    async def wrapper(
            exercise: exercise_type,
            submission: submission_type,
            feedback: feedback_type,
            module_config: Optional[str] = Header(
                None, alias="X-Module-Config"),
            metadata: Dict[str, Any] = Depends(get_meta)):
        if module_config:
            try:
                module_config = json.loads(module_config)
            except json.JSONDecodeError:
                logger.warning(
                    "Invalid module config received: %s", module_config)
                module_config = None

        # Retrieve existing metadata for the exercise, submission and feedback
        exercise.meta.update(get_stored_exercise_meta(exercise) or {})
        submission.meta.update(get_stored_submission_meta(submission) or {})
        feedback.meta.update(get_stored_feedback_meta(feedback) or {})

        store_feedback(feedback)

        args = [exercise, submission, feedback]
        if len(inspect.signature(func).parameters) > 2:
            args.append(module_config)

        # Call the actual consumer
        if inspect.iscoroutinefunction(func):
            await func(*args)
        else:
            func(*args)

        return {"data": None, "meta": metadata}
    return wrapper


def feedback_provider(func: Union[
    Callable[[E, S], List[F]],
    Callable[[E, S, Optional[dict]], List[F]],
    Callable[[E, S], Coroutine[Any, Any, List[F]]],
    Callable[[E, S, Optional[dict]], Coroutine[Any, Any, List[F]]]
]):
    """
    Provide feedback to the Assessment Module Manager.
    The feedback provider is usually called whenever the tutor requests feedback for a submission in the LMS.
    """
    exercise_type = inspect.signature(func).parameters["exercise"].annotation
    submission_type = inspect.signature(
        func).parameters["submission"].annotation

    @app.post("/feedback_suggestions", responses=module_responses)
    @authenticated
    async def wrapper(
            exercise: exercise_type,
            submission: submission_type,
            module_config: Optional[str] = Header(
                None, alias="X-Module-Config"),
            metadata: Dict[str, Any] = Depends(get_meta)):
        if module_config:
            try:
                module_config = json.loads(module_config)
            except json.JSONDecodeError:
                logger.warning(
                    "Invalid module config received: %s", module_config)
                module_config = None

        # Retrieve existing metadata for the exercise, submission and feedback
        exercise.meta.update(get_stored_exercise_meta(exercise) or {})
        submission.meta.update(get_stored_submission_meta(submission) or {})

        store_exercise(exercise)
        store_submissions([submission])

        args = [exercise, submission]
        if len(inspect.signature(func).parameters) > 2:
            args.append(module_config)

        # Call the actual provider
        if inspect.iscoroutinefunction(func):
            feedbacks = await func(*args)
        else:
            feedbacks = func(*args)

        store_feedback_suggestions(feedbacks)
        return {"data": feedbacks, "meta": metadata}
    return wrapper


def config_schema_provider(func: Union[Callable[[], dict], Callable[[], Coroutine[Any, Any, dict]]]):
    """
    Get available configuration options of a module.
    """

    @app.get("/config_schema", responses=module_responses)
    @authenticated
    async def wrapper():
        if inspect.iscoroutinefunction(func):
            config = await func()
        else:
            config = func()
        return config
    return wrapper
