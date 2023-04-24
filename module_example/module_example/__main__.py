from athena import *
from athena.storage import *


@submissions_consumer
def receive_submissions(exercise: Exercise, submissions: List[Submission]):
    print(f"receive_submissions: Received {len(submissions)} submissions for exercise {exercise.id}")
    for submission in submissions:
        print(f"- Submission {submission.id}")
    # Do something with the submissions


@feedback_consumer
def process_incoming_feedback(exercise: Exercise, submission: Submission, feedback: Feedback):
    print(f"process_feedback: Received feedback for submission {submission.id} of exercise {exercise.id}.")
    print(f"process_feedback: Feedback: {feedback}")
    # Do something with the feedback


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
            credits=-1.0,
            meta={},
        )
    ]


if __name__ == "__main__":
    app.start()
