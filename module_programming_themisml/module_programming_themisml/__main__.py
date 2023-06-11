"""
Entry point for the module_example module.
"""
from typing import List

from athena import app, submissions_consumer, submission_selector, feedback_consumer, feedback_provider
from athena.programming import Exercise, Submission, Feedback
from athena.logger import logger
from athena.storage import store_feedback

from .extract_methods import extract_methods


@submissions_consumer
def receive_submissions(exercise: Exercise, submissions: List[Submission]):
    logger.info("receive_submissions: Received %d submissions for exercise %d", len(submissions), exercise.id)


@submission_selector
def select_submission(exercise: Exercise, submissions: List[Submission]) -> Submission:
    logger.info("select_submission: Received %d submissions for exercise %d", len(submissions), exercise.id)
    for submission in submissions:
        logger.info("- Submission %d", submission.id)
    # Do something with the submissions and return the one that should be assessed next
    return submissions[0]


@feedback_consumer
def process_incoming_feedback(exercise: Exercise, submission: Submission, feedback: Feedback):
    logger.info("process_feedback: Received feedback for submission %d of exercise %d", submission.id, exercise.id)
    logger.info("process_feedback: Feedback: %s", feedback)

    if feedback.file_path is None or feedback.line_start is None:
        # cannot process without knowledge about method
        return

    # find method that the feedback is on
    repo_zip = submission.get_zip()
    with repo_zip.open(feedback.file_path, "r") as f:
        file_content = f.read().decode("utf-8")
    methods = extract_methods(file_content)
    feedback_method = None
    for m in methods:
        # method has to contain all feedback lines
        f_start = feedback.line_start
        f_end = feedback.line_end
        if f_end is None:
            f_end = f_start
        if m.line_start <= f_start and m.line_end >= f_end:
            feedback_method = m
            break

    feedback.meta["method_name"] = feedback_method.name if feedback_method else None
    store_feedback(feedback)


@feedback_provider
def suggest_feedback(exercise: Exercise, submission: Submission) -> List[Feedback]:
    logger.info("suggest_feedback: Suggestions for submission %d of exercise %d were requested", submission.id, exercise.id)
    # Do something with the submission and return a list of feedback
    return [
        Feedback(
            id=None,
            exercise_id=exercise.id,
            submission_id=submission.id,
            text="There is something wrong here.",
            detail_text="There is something wrong here.",
            file_path=None,
            line_start=None,
            line_end=None,
            credits=-1.0,
            meta={},
        )
    ]


if __name__ == "__main__":
    app.start()
