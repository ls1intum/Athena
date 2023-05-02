from athena import app, feedback_consumer, feedback_provider, submissions_consumer, submission_selector, ProgrammingExercise
from athena.helpers import get_repository_zip
from athena.storage import *

@submissions_consumer
def receive_submissions(exercise: ProgrammingExercise, submissions: List[Submission]):
    print(f"receive_submissions: Received {len(submissions)} submissions for exercise {exercise.id}")
    for submission in submissions:
        print(f"- Submission {submission.id}")
        with get_repository_zip(submission.content) as zip_content:
            # list the files in the zip
            for file in zip_content.namelist():
                print(f"  - {file}")
    # Do something with the submissions


@submission_selector
def select_submission(exercise: ProgrammingExercise, submissions: List[Submission]) -> Submission:
    print(f"select_submission: Received {len(submissions)} submissions for exercise {exercise.id}")
    for submission in submissions:
        print(f"- Submission {submission.id}")
    # Do something with the submissions and return the one that should be assessed next
    return submissions[0]


@feedback_consumer
def process_incoming_feedback(exercise: ProgrammingExercise, submission: Submission, feedback: Feedback):
    print(f"process_feedback: Received feedback for submission {submission.id} of exercise {exercise.id}.")
    print(f"process_feedback: Feedback: {feedback}")
    # Do something with the feedback


@feedback_provider
def suggest_feedback(exercise: ProgrammingExercise, submission: Submission) -> List[Feedback]:
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
