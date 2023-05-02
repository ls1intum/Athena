from athena import app, submissions_consumer, submission_selector, feedback_consumer, feedback_provider
from athena.helpers import get_programming_submission_zip
from athena.storage import *

from .feedback_provider_registry import FEEDBACK_PROVIDERS

@submissions_consumer
def receive_submissions(exercise: ProgrammingExercise, submissions: List[Submission]):
    print(f"receive_submissions: Received {len(submissions)} submissions for exercise {exercise.id}")
    for submission in submissions:
        print(f"- Submission {submission.id}")
        zip_content = get_programming_submission_zip(submission)
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
    
    approach = exercise.meta.get('approach', 'basic')  # Set 'basic' as the default approach

    if approach not in FEEDBACK_PROVIDERS:
        raise ValueError(f"Unsupported approach '{approach}', supported approaches are {list(FEEDBACK_PROVIDERS.keys())}")

    return FEEDBACK_PROVIDERS[approach](exercise, submission)

if __name__ == "__main__":
    app.start()
