from typing import List, Optional

import nltk

from athena import app, config_schema_provider, submission_selector, submissions_consumer, feedback_consumer, feedback_provider
from athena.text import Exercise, Submission, Feedback
from athena.logger import logger

from module_text_llm.config import Configuration, default_config
from .suggest_feedback_basic import suggest_feedback_basic


@submissions_consumer
def receive_submissions(exercise: Exercise, submissions: List[Submission]):
    logger.info("receive_submissions: Received %d submissions for exercise %d", len(submissions), exercise.id)


@submission_selector
def select_submission(exercise: Exercise, submissions: List[Submission]) -> Submission:
    logger.info("select_submission: Received %d, submissions for exercise %d", len(submissions), exercise.id)
    return submissions[0]


@feedback_consumer
def process_incoming_feedback(exercise: Exercise, submission: Submission, feedback: Feedback):
    logger.info("process_feedback: Received feedback for submission %d of exercise %d.", submission.id, exercise.id)


@feedback_provider
async def suggest_feedback(exercise: Exercise, submission: Submission, module_config: Optional[dict]) -> List[Feedback]:
    logger.info("suggest_feedback: Suggestions for submission %d of exercise %d were requested", submission.id, exercise.id)

    config: Configuration = default_config
    if module_config is not None:
        config = Configuration.parse_obj(module_config)

    return await suggest_feedback_basic(exercise, submission, config.approach, config.debug)


@config_schema_provider
def available_config_schema() -> dict:
    return Configuration.schema()


if __name__ == "__main__":
    nltk.download("punkt")
    app.start()