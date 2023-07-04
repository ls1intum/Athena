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

from module_text_llm.helpers.models import default_model, get_model_from_exercise_meta
from module_text_llm.helpers.utils import add_sentence_numbers, parse_line_number_reference_as_span

from .prompts.suggest_feedback_basic import system_template, human_template


async def suggest_feedback_basic(exercise: Exercise, submission: Submission) -> List[Feedback]:
    model = get_model_from_exercise_meta(exercise)
    if model is None:
        model = default_model
    logger.info("suggest_feedback_basic - model: %s", model)

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

    chain = LLMChain(llm=model, prompt=chat_prompt)
    result = chain.run(**input)
    result = f"reference,credits,text\n{result}"
    reader = csv.DictReader(result.splitlines())

    feedbacks = []
    for row in reader:
        if "reference" not in row or "credits" not in row or "text" not in row:
            logger.warning("Could not parse row %s", row)
            continue

        try:
            credits = float(row["credits"])
        except ValueError:
            logger.warning("Could not parse credits from row %s", row)
            continue
        
        feedbacks.append(Feedback(
            id=None,
            exercise_id=exercise.id,
            submission_id=submission.id,
            detail_text=row["text"],
            reference=parse_line_number_reference_as_span(row["reference"], submission.content),
            credits=credits,
            text="Feedback",
            meta={}
        ))

    return feedbacks