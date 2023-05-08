from athena import app, submissions_consumer, submission_selector, feedback_consumer, feedback_provider
from athena.storage import *

from module_programming_llm.basic.file_instructions import generate_file_grading_instructions, generate_file_problem_statements
from .feedback_provider_registry import FEEDBACK_PROVIDERS


@submissions_consumer
def receive_submissions(exercise: ProgrammingExercise, submissions: List[Submission]):
    print(f"receive_submissions: Received {len(submissions)} submissions for exercise {exercise.id}")

    # TODO Add this later:
    # print("Generating file grading instructions...")
    # file_grading_instructions = generate_file_grading_instructions(exercise)
    # print(file_grading_instructions)
    # exercise.meta['file_grading_instructions'] = file_grading_instructions
    # store_exercise(exercise)

    # generate_file_problem_statement(exercise)

@submission_selector
def select_submission(exercise: ProgrammingExercise, submissions: List[Submission]) -> Submission:
    print(f"select_submission: Received {len(submissions)} submissions for exercise {exercise.id}")
    # Always return the first submission
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

    # TODO remove later
    exercise.meta['file_grading_instructions'] = generate_file_grading_instructions(exercise)
    exercise.meta['file_problem_statements'] = generate_file_problem_statements(exercise)

    approach = exercise.meta.get('approach', 'basic')  # Set 'basic' as the default approach

    if approach not in FEEDBACK_PROVIDERS:
        raise ValueError(f"Unsupported approach '{approach}', supported approaches are {list(FEEDBACK_PROVIDERS.keys())}")

    return FEEDBACK_PROVIDERS[approach](exercise, submission)

if __name__ == "__main__":
    app.start()
