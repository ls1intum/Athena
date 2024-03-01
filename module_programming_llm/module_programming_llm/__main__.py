import os
from typing import List

import tiktoken

from athena import app, submission_selector, submissions_consumer, graded_feedback_consumer, graded_feedback_provider
from athena.endpoints import non_graded_feedback_provider
from athena.programming import Exercise, Submission, GradedFeedback, NonGradedFeedback
from athena.logger import logger
from module_programming_llm.config import Configuration

from module_programming_llm.generate_graded_suggestions_by_file import \
    generate_suggestions_by_file as generate_graded_suggestions_by_file
from module_programming_llm.generate_non_graded_suggestions_by_file import \
    generate_suggestions_by_file as generate_non_graded_suggestions_by_file


@submissions_consumer
def receive_submissions(exercise: Exercise, submissions: List[Submission]):
    logger.info("receive_submissions: Received %d submissions for exercise %d", len(submissions), exercise.id)


@submission_selector
def select_submission(exercise: Exercise, submissions: List[Submission]) -> Submission:
    logger.info("select_submission: Received %d, submissions for exercise %d", len(submissions), exercise.id)
    return submissions[0]


@graded_feedback_consumer
def process_incoming_feedback(exercise: Exercise, submission: Submission, feedbacks: List[GradedFeedback]):
    logger.info("process_feedback: Received %d feedbacks for submission %d of exercise %d.", len(feedbacks),
                submission.id, exercise.id)


@graded_feedback_provider
async def suggest_graded_feedback(exercise: Exercise, submission: Submission, module_config: Configuration) -> \
        List[GradedFeedback]:
    logger.info("suggest_feedback: graded suggestions for submission %d of exercise %d were requested", submission.id,
                exercise.id)
    return await generate_graded_suggestions_by_file(exercise, submission, module_config.graded_approach,
                                                     module_config.debug)

@non_graded_feedback_provider
async def suggest_non_graded_feedback(exercise: Exercise, submission: Submission, module_config: Configuration) -> \
        List[NonGradedFeedback]:
    logger.info("suggest_feedback: non graded suggestions for submission %d of exercise %d were requested",
                submission.id, exercise.id)
    return await generate_non_graded_suggestions_by_file(exercise, submission, module_config.non_graded_approach,
                                                         module_config.debug)


if __name__ == "__main__":
    # Preload for token estimation later
    tiktoken.get_encoding("cl100k_base")
    app.start()
