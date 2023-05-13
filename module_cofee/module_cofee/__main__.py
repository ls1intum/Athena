"""
Entry point for the module_cofee module.
"""
from typing import List

from athena import app, submission_selector, submissions_consumer, feedback_consumer, feedback_provider
from athena.text import Exercise, Submission, Feedback

from module_cofee import adapter


@submission_selector
def select_submission(exercise: Exercise, submissions: List[Submission]) -> Submission:
    print(f"select_submission: Received {len(submissions)} submissions for exercise {exercise.id}")
    for submission in submissions:
        print(f"- Submission {submission.id}")
    # TODO: select submission with highest information gain
    # For now, just return the first one:
    return submissions[0]


@submissions_consumer
def receive_submissions(exercise: Exercise, submissions: List[Submission]):
    print(f"receive_submissions: Received {len(submissions)} submissions for exercise {exercise.id}")
    adapter.send_submissions(exercise, submissions)


@feedback_consumer
def process_incoming_feedback(exercise: Exercise, submission: Submission, feedback: Feedback):
    # no need to do anything here, the feedback is automatically stored in the database
    pass


@feedback_provider
def suggest_feedback(exercise: Exercise, submission: Submission) -> List[Feedback]:
    print(f"suggest_feedback: Suggestions for submission {submission.id} of exercise {exercise.id} were requested")
    # Do something with the submission and return a list of feedback
    return [
        Feedback(
            id=10,
            exercise_id=exercise.id,
            submission_id=submission.id,
            detail_text="There is something wrong here.",
            text="Correct",
            reference=None,
            credits=-1.0,
            meta={},
        )
    ]


if __name__ == "__main__":
    app.start()
