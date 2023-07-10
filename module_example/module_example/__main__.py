"""
Entry point for the module_example module.
"""
from ast import Dict
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

from athena import app, config_schema_provider, submissions_consumer, submission_selector, feedback_consumer, feedback_provider, emit_meta
from athena.programming import Exercise, Submission, Feedback
from athena.logger import logger
from athena.storage import store_exercise, store_submissions, store_feedback


class Configuration(BaseModel):
    """Example configuration for the module_example module."""
    debug: bool = Field(False, description="Whether the module is in debug mode. This is an example config option.")


@submissions_consumer
def receive_submissions(exercise: Exercise, submissions: List[Submission], module_config: Optional[dict]):
    logger.info("receive_submissions: Received %d submissions for exercise %d", len(
        submissions), exercise.id)
    for submission in submissions:
        logger.info("- Submission %d", submission.id)
        zip_content = submission.get_zip()
        # list the files in the zip
        for file in zip_content.namelist():
            logger.info("  - %s", file)
    # Do something with the submissions
    logger.info("Doing stuff")

    # Example use module config
    if module_config is not None:
        config = Configuration.parse_obj(module_config)
        logger.info("Config: %s", config)
        if config.debug:
            emit_meta('debug', True)
            emit_meta('_comment', 'You can add any meta data you want here')
    else:
        logger.info("No config")

    # Add data to exercise
    exercise.meta["some_data"] = "some_value"
    logger.info("- Exercise meta: %s", exercise.meta)

    # Add data to submission
    for submission in submissions:
        submission.meta["some_data"] = "some_value"
        logger.info("- Submission %d meta: %s", submission.id, submission.meta)

    store_exercise(exercise)
    store_submissions(submissions)


@submission_selector
def select_submission(exercise: Exercise, submissions: List[Submission]) -> Submission:
    logger.info("select_submission: Received %d submissions for exercise %d", len(
        submissions), exercise.id)
    for submission in submissions:
        logger.info("- Submission %d", submission.id)
    # Do something with the submissions and return the one that should be assessed next
    return submissions[0]


@feedback_consumer
def process_incoming_feedback(exercise: Exercise, submission: Submission, feedback: Feedback):
    logger.info("process_feedback: Received feedback for submission %d of exercise %d",
                submission.id, exercise.id)
    logger.info("process_feedback: Feedback: %s", feedback)
    # Do something with the feedback
    # Add data to feedback
    feedback.meta["some_data"] = "some_value"

    store_feedback(feedback)


@feedback_provider
def suggest_feedback(exercise: Exercise, submission: Submission, module_config: Optional[dict]) -> List[Feedback]:
    logger.info("suggest_feedback: Suggestions for submission %d of exercise %d were requested",
                submission.id, exercise.id)
    # Do something with the submission and return a list of feedback

    # Example use of module config
    if module_config is not None:
        config = Configuration.parse_obj(module_config)
        logger.info("Config: %s", config)
        if config.debug:
            emit_meta('costs', '100.00€')

    return [
        Feedback(
            exercise_id=exercise.id,
            submission_id=submission.id,
            detail_text="There is something wrong here.",
            file_path=None,
            line=None,
            credits=-1.0,
            meta={},
        )
    ]


# Optional: Provide configuration options for the module
@config_schema_provider
def available_config_schema() -> dict:
    # Custom configuration options
    # Ideally return a schema RFC8927 compliant json schema or something similar
    # pydantic with `.schema()` mostly does the job
    return Configuration.schema()


if __name__ == "__main__":
    app.start()
