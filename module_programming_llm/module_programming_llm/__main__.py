from athena.storage import *

from athena import app, submission_selector, submissions_consumer, feedback_consumer, feedback_provider
from athena.programming import *

from module_programming_llm.basic.file_instructions import generate_file_grading_instructions, generate_file_problem_statements
from module_programming_llm.basic.basic_feedback_provider import suggest_feedback as suggest_feedback_basic


@submission_selector
def select_submission(exercise: Exercise, submissions: List[Submission]) -> Submission:
    print(f"select_submission: Received {len(submissions)} submissions for exercise {exercise.id}")
    # Always return the first submission
    return submissions[0]


@submissions_consumer
def receive_submissions(exercise: Exercise, submissions: List[Submission]):
    print(f"receive_submissions: Received {len(submissions)} submissions for exercise {exercise.id}")

    # TODO Add this later:
    # print("Generating file grading instructions...")
    # file_grading_instructions = generate_file_grading_instructions(exercise)
    # print(file_grading_instructions)
    # exercise.meta['file_grading_instructions'] = file_grading_instructions
    # store_exercise(exercise)

    # generate_file_problem_statement(exercise)


@feedback_consumer
def process_incoming_feedback(exercise: Exercise, submission: Submission, feedback: Feedback):
    print(f"process_feedback: Received feedback for submission {submission.id} of exercise {exercise.id}.")
    print(f"process_feedback: Feedback: {feedback}")
    # Do something with the feedback


@feedback_provider
def suggest_feedback(exercise: Exercise, submission: Submission) -> List[Feedback]:
    print(f"suggest_feedback: Suggestions for submission {submission.id} of exercise {exercise.id} were requested")
    # Do something with the submission and return a list of feedback

    # TODO remove later
    exercise.meta['file_grading_instructions'] = generate_file_grading_instructions(exercise)
    exercise.meta['file_problem_statements'] = generate_file_problem_statements(exercise)

    return suggest_feedback_basic(exercise, submission)

if __name__ == "__main__":
    app.start()
