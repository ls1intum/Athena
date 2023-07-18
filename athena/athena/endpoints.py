# type: ignore # too much weird behavior of mypy with decorators
import inspect
from fastapi import Depends
from pydantic import BaseModel, ValidationError
from typing import TypeVar, Callable, List, Union, Any, Coroutine, Type

from pydantic import BaseModel

from athena.app import app
from athena.authenticate import authenticated
from athena.metadata import with_meta
from athena.module_config import get_dynamic_module_config_factory
from athena.logger import logger
from athena.schemas import Exercise, Submission, Feedback
from athena.schemas.schema import to_camel
from athena.storage import get_stored_submission_meta, get_stored_exercise_meta, get_stored_feedback_meta, \
    store_exercise, store_feedback, store_feedback_suggestions, store_submissions, get_stored_submissions


E = TypeVar('E', bound=Exercise)
S = TypeVar('S', bound=Submission)
F = TypeVar('F', bound=Feedback)

# Config type
C = TypeVar("C", bound=BaseModel)

module_responses = {
    403: {
        "description": "API secret is invalid - set the environment variable SECRET and the Authorization header "
                       "to the same value",
    }
}


def submissions_consumer(func: Union[
    Callable[[E, List[S]], None],
    Callable[[E, List[S]], Coroutine[Any, Any, None]],
    Callable[[E, List[S], C], None],
    Callable[[E, List[S], C], Coroutine[Any, Any, None]]
]):
    """
    Receive submissions from the Assessment Module Manager.
    The submissions consumer is usually called whenever the deadline for an exercise is reached.
    
    This decorator can be used with several types of functions: synchronous or asynchronous, with or without a module config.

    Examples:
        Below are some examples of possible functions that you can decorate with this decorator:

        Without using module config (both synchronous and asynchronous forms):
        >>> @submissions_consumer
        ... def sync_receive_submissions(exercise: Exercise, submissions: List[Submission]):
        ...     # process submissions synchronously here

        >>> @submissions_consumer
        ... async def async_receive_submissions(exercise: Exercise, submissions: List[Submission]):
        ...     # process submissions asynchronously here

        With using module config (both synchronous and asynchronous forms):
        >>> @submissions_consumer
        ... def sync_receive_submissions_with_config(exercise: Exercise, submissions: List[Submission], module_config: Optional[dict]):
        ...     # process submissions synchronously here using module_config

        >>> @submissions_consumer
        ... async def async_receive_submissions_with_config(exercise: Exercise, submissions: List[Submission], module_config: Optional[dict]):
        ...     # process submissions asynchronously here using module_config
    """
    exercise_type = inspect.signature(func).parameters["exercise"].annotation
    submission_type = inspect.signature(func).parameters["submissions"].annotation.__args__[0]
    module_config_type = inspect.signature(func).parameters["module_config"].annotation if "module_config" in inspect.signature(func).parameters else None

    @app.post("/submissions", responses=module_responses)
    @authenticated
    @with_meta
    async def wrapper(
            exercise: exercise_type,
            submissions: List[submission_type],
            module_config: module_config_type = Depends(get_dynamic_module_config_factory(module_config_type))):
        
        # Retrieve existing metadata for the exercise and submissions
        exercise_meta = get_stored_exercise_meta(exercise) or {}
        exercise_meta.update(exercise.meta)
        exercise.meta = exercise_meta
        submissions_dict = {s.id: s for s in submissions}
        if submissions:
            stored_submissions = get_stored_submissions(
                submissions[0].__class__, exercise.id, [s.id for s in submissions])
            for stored_submission in stored_submissions:
                if stored_submission.id in submissions_dict:
                    submission_meta = get_stored_submission_meta(stored_submission) or {}
                    submission_meta.update(stored_submission.meta)
                    submissions_dict[stored_submission.id].meta = submission_meta
        submissions = list(submissions_dict.values())
        store_submissions(submissions)

        store_exercise(exercise)
        store_submissions(submissions)

        kwargs = {}
        if "module_config" in inspect.signature(func).parameters:
            kwargs["module_config"] = module_config

        store_exercise(exercise)
        store_submissions(submissions)

        kwargs = {}
        if "module_config" in inspect.signature(func).parameters:
            kwargs["module_config"] = module_config

        # Call the actual consumer
        if inspect.iscoroutinefunction(func):
            await func(exercise, submissions, **kwargs)
        else:
            func(exercise, submissions, **kwargs)

        return None
    return wrapper


def submission_selector(func: Union[
    Callable[[E, List[S]], S],
    Callable[[E, List[S]], Coroutine[Any, Any, S]],
    Callable[[E, List[S], C], S],
    Callable[[E, List[S], C], Coroutine[Any, Any, S]]
]):
    """
    Receive an exercise and some (not necessarily all!) submissions from the Assessment Module Manager and
    return the submission that should ideally be assessed next.
    If the selector returns None, the LMS will select a random submission in the end.

    This decorator can be used with several types of functions: synchronous or asynchronous, with or without a module config.

    Examples:
        Below are some examples of possible functions that you can decorate with this decorator:

        Without using module config (both synchronous and asynchronous forms):
        >>> @submission_selector
        ... def sync_select_submission(exercise: Exercise, submissions: List[Submission]):
        ...     # process submissions here and return the chosen submission

        >>> @submission_selector
        ... async def async_select_submission(exercise: Exercise, submissions: List[Submission]):
        ...     # process submissions here and return the chosen submission

        With using module config (both synchronous and asynchronous forms):
        >>> @submission_selector
        ... def sync_select_submission_with_config(exercise: Exercise, submissions: List[Submission], module_config: Optional[dict]):
        ...     # process submissions here using module_config and return the chosen submission

        >>> @submission_selector
        ... async def async_select_submission_with_config(exercise: Exercise, submissions: List[Submission], module_config: Optional[dict]):
        ...     # process submissions here using module_config and return the chosen submission
    """
    exercise_type = inspect.signature(func).parameters["exercise"].annotation
    submission_type = inspect.signature(func).parameters["submissions"].annotation.__args__[0]
    module_config_type = inspect.signature(func).parameters["module_config"].annotation if "module_config" in inspect.signature(func).parameters else None

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
    @with_meta
    async def wrapper(
            exercise: exercise_type,
            submission_ids: List[int],
            module_config: module_config_type = Depends(get_dynamic_module_config_factory(module_config_type))):
        # The wrapper handles only transmitting submission IDs for efficiency, but the actual selection logic
        # only works with the full submission objects.

        exercise.meta.update(get_stored_exercise_meta(exercise) or {})
        store_exercise(exercise)

        # Get the full submission objects
        submissions = list(get_stored_submissions(submission_type, exercise.id, submission_ids))
        if len(submission_ids) != len(submissions):
            logger.warning("Not all submissions were found in the database! "
                           "Have you sent all submissions to the submission consumer before?")
        if not submissions:
            # Nothing to select from
            return -1

        kwargs = {}
        if "module_config" in inspect.signature(func).parameters:
            kwargs["module_config"] = module_config

        # Select the submission
        if inspect.iscoroutinefunction(func):
            submission = await func(exercise, submissions, **kwargs)
        else:
            submission = func(exercise, submissions, **kwargs)

        if submission is None:
            return -1
        return submission.id

    return wrapper


def feedback_consumer(func: Union[
    Callable[[E, S, List[F]], None],
    Callable[[E, S, List[F]], Coroutine[Any, Any, None]],
    Callable[[E, S, List[F], C], None],
    Callable[[E, S, List[F], C], Coroutine[Any, Any, None]]
]):
    """
    Receive feedback from the Assessment Module Manager.
    The feedback consumer is usually called whenever the LMS gets feedback from a tutor.

    This decorator can be used with several types of functions: synchronous or asynchronous, with or without a module config.

    Examples:
        Below are some examples of possible functions that you can decorate with this decorator:

        Without using module config (both synchronous and asynchronous forms):
        >>> @feedback_consumer
        ... def sync_process_feedback(exercise: Exercise, submission: Submission, feedbacks: List[Feedback]):
        ...     # process feedback here

        >>> @feedback_consumer
        ... async def async_process_feedback(exercise: Exercise, submission: Submission, feedbacks: List[Feedback]):
        ...     # process feedback here

        With using module config (both synchronous and asynchronous forms):
        >>> @feedback_consumer
        ... def sync_process_feedback_with_config(exercise: Exercise, submission: Submission, feedbacks: List[Feedback], module_config: Optional[dict]):
        ...     # process feedback here using module_config

        >>> @feedback_consumer
        ... async def async_process_feedback_with_config(exercise: Exercise, submission: Submission, feedbacks: List[Feedback], module_config: Optional[dict]):
        ...     # process feedback here using module_config
    """
    exercise_type = inspect.signature(func).parameters["exercise"].annotation
    submission_type = inspect.signature(func).parameters["submission"].annotation
    feedback_type = inspect.signature(func).parameters["feedbacks"].annotation.__args__[0]
    module_config_type = inspect.signature(func).parameters["module_config"].annotation if "module_config" in inspect.signature(func).parameters else None

    @app.post("/feedbacks", responses=module_responses)
    @authenticated
    @with_meta
    async def wrapper(
            exercise: exercise_type,
            submission: submission_type,
            feedbacks: List[feedback_type],
            module_config: module_config_type = Depends(get_dynamic_module_config_factory(module_config_type))):

        # Retrieve existing metadata for the exercise, submission and feedback
        exercise.meta.update(get_stored_exercise_meta(exercise) or {})
        store_exercise(exercise)
        submission.meta.update(get_stored_submission_meta(submission) or {})
        store_submissions([submission])
        for feedback in feedbacks:
            feedback.meta.update(get_stored_feedback_meta(feedback) or {})
            store_feedback(feedback)

        kwargs = {}
        if "module_config" in inspect.signature(func).parameters:
            kwargs["module_config"] = module_config

        kwargs = {}
        if "module_config" in inspect.signature(func).parameters:
            kwargs["module_config"] = module_config

        # Call the actual consumer
        if inspect.iscoroutinefunction(func):
            await func(exercise, submission, feedback, **kwargs)
        else:
            func(exercise, submission, feedbacks, **kwargs)

        return None
    return wrapper


def feedback_provider(func: Union[
    Callable[[E, S], List[F]],
    Callable[[E, S], Coroutine[Any, Any, List[F]]],
    Callable[[E, S, C], List[F]],
    Callable[[E, S, C], Coroutine[Any, Any, List[F]]]
]):
    """
    Provide feedback to the Assessment Module Manager.
    The feedback provider is usually called whenever the tutor requests feedback for a submission in the LMS.

    This decorator can be used with several types of functions: synchronous or asynchronous, with or without a module config.

    Examples:
        Below are some examples of possible functions that you can decorate with this decorator:

        Without using module config (both synchronous and asynchronous forms):
        >>> @feedback_provider
        ... def sync_suggest_feedback(exercise: Exercise, submission: Submission):
        ...     # suggest feedback here and return it as a list

        >>> @feedback_provider
        ... async def async_suggest_feedback(exercise: Exercise, submission: Submission):
        ...     # suggest feedback here and return it as a list

        With using module config (both synchronous and asynchronous forms):
        >>> @feedback_provider
        ... def sync_suggest_feedback_with_config(exercise: Exercise, submission: Submission, module_config: Optional[dict]):
        ...     # suggest feedback here using module_config and return it as a list

        >>> @feedback_provider
        ... async def async_suggest_feedback_with_config(exercise: Exercise, submission: Submission, module_config: Optional[dict]):
        ...     # suggest feedback here using module_config and return it as a list
    """
    exercise_type = inspect.signature(func).parameters["exercise"].annotation
    submission_type = inspect.signature(func).parameters["submission"].annotation
    module_config_type = inspect.signature(func).parameters["module_config"].annotation if "module_config" in inspect.signature(func).parameters else None

    @app.post("/feedback_suggestions", responses=module_responses)
    @authenticated
    @with_meta
    async def wrapper(
            exercise: exercise_type,
            submission: submission_type,
            module_config: module_config_type = Depends(get_dynamic_module_config_factory(module_config_type))):
        
        # Retrieve existing metadata for the exercise, submission and feedback
        exercise.meta.update(get_stored_exercise_meta(exercise) or {})
        submission.meta.update(get_stored_submission_meta(submission) or {})

        store_exercise(exercise)
        store_submissions([submission])

        kwargs = {}
        if "module_config" in inspect.signature(func).parameters:
            kwargs["module_config"] = module_config

        # Call the actual provider
        if inspect.iscoroutinefunction(func):
            feedbacks = await func(exercise, submission, **kwargs)
        else:
            feedbacks = func(exercise, submission, **kwargs)

        store_feedback_suggestions(feedbacks)

        return feedbacks
    return wrapper


def config_schema_provider(cls: Type[C]) -> Type[C]:
    """
    Decorator for a class to provide an endpoint that returns the configuration class schema.

    The decorated class must be a subclass of BaseModel and must have default values for all parameters (default configuration).

    Example:
        >>> @config_schema_provider
        ... class MyConfig(BaseModel):
        ...     my_parameter: str = "default value"
    """
    if not issubclass(cls, BaseModel):
        raise TypeError("Decorated class must be a subclass of BaseModel")

    if getattr(app.state, "config_schema_defined", False):
        raise ValueError("@config_schema_provider can only be used once")

    # Try to initialize the class without parameters (default values will be used)
    try:
        cls()
    except ValidationError as exc:
        raise TypeError(f'Cannot initialize {cls.__name__} without parameters, please provide default values for all parameters') from exc

    @app.get("/config_schema")
    async def wrapper():
        return cls.schema()

    app.state.config_schema_defined = True
    return cls