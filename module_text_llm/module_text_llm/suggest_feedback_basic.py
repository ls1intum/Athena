import csv
from typing import List

from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from athena.text import Exercise, Submission, Feedback
from athena.logger import logger

from module_text_llm.helpers.models import chat
from module_text_llm.helpers.utils import add_sentence_numbers

from .prompts.suggest_feedback_basic import system_template, human_template


async def suggest_feedback_basic(exercise: Exercise, submission: Submission) -> List[Feedback]:
    input = {
        "max_points": exercise.max_points,
        "bonus_points": exercise.bonus_points,
        "grading_instructions": exercise.grading_instructions,
        "problem_statement": exercise.problem_statement,
        # TODO: "example_solution": exercise.example_solution, MISSING
        "submission_with_sentence_numbers": add_sentence_numbers(submission.content)
    }

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    logger.info(chat_prompt.format_messages(**input))

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(**input)
    logger.info(result)
    result = f"reference,credits,text\n{result}"
    reader = csv.DictReader(result.splitlines())

    return [Feedback(
        id=None,
        exercise_id=exercise.id,
        submission_id=submission.id,
        detail_text=row["text"],
        reference=row["reference"],
        credits=float(row["credits"]),
        text="Feedback",
        meta={}
    ) for row in reader]