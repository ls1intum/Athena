"""
Entry point for the module_programming_ast module.
"""
import random
from typing import List, Any, cast
from pydantic import BaseModel, Field

from athena import app, config_schema_provider, submissions_consumer, submission_selector, feedback_consumer, \
    feedback_provider, evaluation_provider, emit_meta
from athena.programming import Exercise, Submission, Feedback, get_stored_submissions
from athena.logger import logger
from athena.storage import store_exercise, store_submissions, store_feedback
from module_programming_ast.convert_code_to_ast.get_feedback_methods import get_feedback_method
from module_programming_ast.feedback_suggestions.feedback_suggestions import create_feedback_suggestions


@config_schema_provider
class Configuration(BaseModel):
    """Example configuration for the module_programming_ast module."""
    debug: bool = Field(False, description="Whether the module is in **debug mode**. This is an example config option.")


@submissions_consumer
def receive_submissions(exercise: Exercise, submissions: List[Submission], module_config: Configuration):
    logger.info("receive_submissions: Received %d submissions for exercise %d", len(submissions), exercise.id)
    for submission in submissions:
        logger.info("- Submission %d", submission.id)
        zip_content = submission.get_zip()
        # list the files in the zip
        for file in zip_content.namelist():
            logger.info("  - %s", file)
    # Do something with the submissions
    logger.info("Doing stuff")

    # Example use module config
    # If you are not using module_config for your module, you can remove it from the function signature
    logger.info("Config: %s", module_config)
    if module_config.debug:
        emit_meta('debug', True)
        emit_meta('comment', 'You can add any metadata you want here')

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
    logger.info("select_submission: Received %d submissions for exercise %d", len(submissions), exercise.id)
    for submission in submissions:
        logger.info("- Submission %d", submission.id)
    # Do something with the submissions and return the one that should be assessed next
    return submissions[0]


@feedback_consumer
def process_incoming_feedback(exercise: Exercise, submission: Submission, feedbacks: List[Feedback]):
    logger.info("process_feedback: Received %d feedbacks for submission %d of exercise %d", len(feedbacks),
                submission.id, exercise.id)
    logger.info("process_feedback: Feedbacks: %s", feedbacks)

    programming_language = exercise.programming_language.lower()
    # Currently only works with Java and Python - can be extended with more languages if the grammar is available
    if programming_language not in ["java", "python"]:
        logger.info("AP-TED currently only works with Java and Python. Not consuming feedback.")
        return

    # Remove unreferenced feedbacks
    feedbacks = list(filter(lambda f: f.file_path is not None and f.line_start is not None, feedbacks))

    # Add method metadata to feedbacks
    feedbacks_with_method = []
    for feedback in feedbacks:
        feedback_method = get_feedback_method(submission, feedback, programming_language)
        if feedback_method is None:
            # don't consider feedback without a method
            continue
        logger.debug("Feedback #%d: Found method %s", feedback.id, feedback_method.name)
        feedback.meta["method_name"] = feedback_method.name
        feedback.meta["method_code"] = feedback_method.source_code
        feedback.meta["method_line_start"] = feedback_method.line_start
        feedback.meta["method_line_end"] = feedback_method.line_end
        feedback.meta["method_ast"] = feedback_method.ast
        feedbacks_with_method.append(feedback)
    feedbacks = feedbacks_with_method

    # find all submissions for this exercise
    exercise_submissions = cast(List[Submission], list(get_stored_submissions(exercise.id)))

    # create feedback suggestions
    logger.info("Creating feedback suggestions for %d feedbacks", len(feedbacks))
    feedback_suggestions = create_feedback_suggestions(exercise_submissions, feedbacks)

    # additionally, store metadata about how impactful each feedback was, i.e. how many suggestions were given based on it
    for feedback in feedbacks:
        # count how many suggestions were given based on this feedback
        feedback.meta["n_feedback_suggestions"] = len(
            [f for f in feedback_suggestions if f.meta["original_feedback_id"] == feedback.id])
        # store the information on the suggestions as well for quicker access later
        for suggestion in feedback_suggestions:
            if suggestion.meta["original_feedback_id"] == feedback.id:
                suggestion.meta["n_feedback_suggestions"] = feedback.meta["n_feedback_suggestions"]

    # save to database
    store_feedback_suggestions(feedback_suggestions)  # type: ignore
    for feedback in feedbacks:
        store_feedback(feedback)

    logger.debug("Feedbacks processed")


@feedback_provider
def suggest_feedback(exercise: Exercise, submission: Submission, module_config: Configuration) -> List[Feedback]:
    logger.info("suggest_feedback: Suggestions for submission %d of exercise %d were requested", submission.id,
                exercise.id)
    # Do something with the submission and return a list of feedback

    # Example use of module config
    # If you are not using module_config for your module, you can remove it from the function signature
    logger.info("Config: %s", module_config)
    if module_config.debug:
        emit_meta("costs", "100.00€")

    return [
        # Referenced feedback, line 8-9 in BinarySearch.java
        Feedback(
            id=None,
            exercise_id=exercise.id,
            submission_id=submission.id,
            title="This is a suggestion.",
            description="There is something wrong here.",
            credits=-1.0,
            file_path="BinarySearch.java",
            line_start=8,
            line_end=9,
            structured_grading_instruction_id=None,
            meta={}
        ),
        # Referenced feedback, line 13-18 in BinarySearch.java
        Feedback(
            id=None,
            exercise_id=exercise.id,
            submission_id=submission.id,
            title="This is a second suggestion.",
            description="This is very good!",
            credits=2.0,
            file_path="BinarySearch.java",
            line_start=13,
            line_end=18,
            structured_grading_instruction_id=None,
            meta={}
        ),
        # Unreferenced feedback without file
        Feedback(
            id=None,
            exercise_id=exercise.id,
            submission_id=submission.id,
            title="This is an unreferenced suggestion.",
            description="General feedback without any reference to the submission.",
            credits=0.0,
            file_path=None,
            line_start=None,
            line_end=None,
            structured_grading_instruction_id=None,
            meta={}
        ),
        # Unreferenced feedback in BinarySearch.java
        Feedback(
            id=None,
            exercise_id=exercise.id,
            submission_id=submission.id,
            title="This is an unreferenced suggestion in a file.",
            description="General feedback with only the reference to a file (BinarySearch.java)",
            credits=0.0,
            file_path="BinarySearch.java",
            line_start=None,
            line_end=None,
            structured_grading_instruction_id=None,
            meta={}
        )
    ]


# Only if it makes sense for a module (Optional)
@evaluation_provider
def evaluate_feedback(exercise: Exercise, submission: Submission, true_feedbacks: List[Feedback],
                      predicted_feedbacks: List[Feedback]) -> Any:
    logger.info(
        "evaluate_feedback: Evaluation for submission %d of exercise %d was requested with %d true and %d predicted feedbacks",
        submission.id, exercise.id, len(true_feedbacks), len(predicted_feedbacks)
    )

    # Do something with the true and predicted feedback and return the evaluation result
    # Generate some example evaluation result
    evaluation_results = []
    true_feedback_embeddings = [random.random() for _ in true_feedbacks]
    predicted_feedback_embeddings = [random.random() for _ in predicted_feedbacks]
    for feedback, embedding in zip(predicted_feedbacks, predicted_feedback_embeddings):
        feedback_evaluation = {
            "feedback_id": feedback.id,
            "embedding": embedding,
            "has_match": len([t for t in true_feedback_embeddings if abs(t - embedding) < 0.1]) > 0,
            "correctness": random.random()
        }
        evaluation_results.append(feedback_evaluation)

    return evaluation_results


if __name__ == "__main__":
    app.start()
