from athena import *
from athena.helpers import get_programming_submission_zip
from athena.storage import *

from langchain.callbacks import get_openai_callback
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessage,
    SystemMessage,
)

import json

from langchain.output_parsers import PydanticOutputParser

from .llm_feedback import LLMFeedback, ListLLMFeedback
from .utils import add_line_numbers

parser = PydanticOutputParser(pydantic_object=ListLLMFeedback)


@submissions_consumer
def receive_submissions(exercise: Exercise, submissions: List[Submission]):
    print(
        f"receive_submissions: Received {len(submissions)} submissions for exercise {exercise.id}")
    for submission in submissions:
        print(f"- Submission {submission.id}")
        zip_content = get_programming_submission_zip(submission)
        # list the files in the zip
        for file in zip_content.namelist():
            print(f"  - {file}")
    # Do something with the submissions


@submission_selector
def select_submission(exercise: Exercise, submissions: List[Submission]) -> Submission:
    print(
        f"select_submission: Received {len(submissions)} submissions for exercise {exercise.id}")
    for submission in submissions:
        print(f"- Submission {submission.id}")
    # Do something with the submissions and return the one that should be assessed next
    return submissions[0]


@feedback_consumer
def process_incoming_feedback(exercise: Exercise, submission: Submission, feedback: Feedback):
    print(
        f"process_feedback: Received feedback for submission {submission.id} of exercise {exercise.id}.")
    print(f"process_feedback: Feedback: {feedback}")
    # Do something with the feedback


@feedback_provider
def suggest_feedback(exercise: Exercise, submission: Submission) -> List[Feedback]:
    print(
        f"suggest_feedback: Suggestions for submission {submission.id} of exercise {exercise.id} were requested")
    # Do something with the submission and return a list of feedback

    chat = ChatOpenAI(temperature=0.7, max_tokens=500)

    feedback = []
    submission_zip = get_programming_submission_zip(submission)
    # list the files in the zip
    for file in submission_zip.namelist():
        # get the content of a file
        content = submission_zip.read(file)

        chat_prompt = [
            SystemMessage(
                content=f"""You are a skilled tutor at a renowned university tasked to grade the following programming exercise submission. Be fair, detailed, objective, critical, smart, and constructive! 

                        The credits' absolute total should be 10!
                        """
            ),
            HumanMessage(content=f"""Student's submission to grade:
                    {add_line_numbers(content)}

                    Only give me the response in the following format, DO NOT ADD ANYTHING ELSE JUST RESPOND WITH ONLY THE JSON OBJECT:
                    {parser.get_format_instructions()}
                    """)
        ]

        with get_openai_callback() as cb:
            output = chat(chat_prompt)
            print(output)
            try:
                feedback = json.loads(output.content)['feedback']
            except Exception as e:
                print(e)
            print(f"Total cost: {cb.total_cost}")

    return [
        Feedback(
            id=0,
            exercise_id=exercise.id,
            submission_id=submission.id,
            credits=0,
            detail_text='',
            text='',
            meta=fb
        )
        for fb in feedback
    ]

if __name__ == "__main__":
    app.start()
