from typing import List

from athena.storage import store_exercise

from athena import app, submission_selector, submissions_consumer, feedback_consumer, feedback_provider
from athena.programming import Exercise, Submission, Feedback

from module_programming_llm.basic.basic_feedback_provider import suggest_feedback as suggest_feedback_basic
from module_programming_llm.basic.file_instructions import generate_file_grading_instructions, generate_file_problem_statements


@submission_selector
def select_submission(exercise: Exercise, submissions: List[Submission]) -> Submission:
    print(f"select_submission: Received {len(submissions)} submissions for exercise {exercise.id}")
    # Always return the first submission
    return submissions[0]


@submissions_consumer
def receive_submissions(exercise: Exercise, submissions: List[Submission]):
    print(f"receive_submissions: Received {len(submissions)} submissions for exercise {exercise.id}")

    # Split problem statements and grading instructions 
    exercise.meta['file_grading_instructions'] = generate_file_grading_instructions(exercise)
    exercise.meta['file_problem_statements'] = generate_file_problem_statements(exercise)
    print(exercise.meta['file_grading_instructions'])
    print(exercise.meta['file_problem_statements'])

    store_exercise(exercise)


@feedback_consumer
def process_incoming_feedback(exercise: Exercise, submission: Submission, feedback: Feedback):
    print(f"process_feedback: Received feedback for submission {submission.id} of exercise {exercise.id}.")
    print(f"process_feedback: Feedback: {feedback}")
    # Do something with the feedback


@feedback_provider
async def suggest_feedback(exercise: Exercise, submission: Submission) -> List[Feedback]:
    print(f"suggest_feedback: Suggestions for submission {submission.id} of exercise {exercise.id} were requested")
    # Do something with the submission and return a list of feedback

    # Check if file based grading instructions and problem statements are available
    if 'file_grading_instructions' in exercise.meta and 'file_problem_statements' in exercise.meta:
        return await suggest_feedback_basic(exercise, submission)
    print("suggest_feedback: No file based grading instructions and problem statements available. Skipping feedback generation.")
    return []

if __name__ == "__main__":
    app.start()
