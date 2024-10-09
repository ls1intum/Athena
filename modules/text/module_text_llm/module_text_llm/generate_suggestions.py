from typing import List, Optional, Sequence
from pydantic import BaseModel, Field

from athena import emit_meta
from athena.text import Exercise, Submission, Feedback
from athena.logger import logger

from module_text_llm.config import BasicApproachConfig
from llm_core.utils.llm_utils import (
    get_chat_prompt_with_formatting_instructions, 
    check_prompt_length_and_omit_features_if_necessary, 
    num_tokens_from_prompt,
)
from llm_core.utils.predict_and_parse import predict_and_parse

from module_text_llm.helpers.utils import add_sentence_numbers, get_index_range_from_line_range, format_grading_instructions

class FeedbackModel(BaseModel):
    title: str = Field(description="Very short title, i.e. feedback category or similar", example="Logic Error")
    description: str = Field(description="Feedback description")
    line_start: Optional[int] = Field(description="Referenced line number start, or empty if unreferenced")
    line_end: Optional[int] = Field(description="Referenced line number end, or empty if unreferenced")
    credits: float = Field(0.0, description="Number of points received/deducted")
    grading_instruction_id: Optional[int] = Field(
        description="ID of the grading instruction that was used to generate this feedback, or empty if no grading instruction was used"
    )

    class Config:
        title = "Feedback"


class AssessmentModel(BaseModel):
    """Collection of feedbacks making up an assessment"""
    
    feedbacks: Sequence[FeedbackModel] = Field(description="Assessment feedbacks")

    class Config:
        title = "Assessment"


async def generate_suggestions(exercise: Exercise, submission: Submission, config: BasicApproachConfig, debug: bool) -> List[Feedback]:
    model = config.model.get_model()  # type: ignore[attr-defined]

    prompt_input = {
        "max_points": exercise.max_points,
        "bonus_points": exercise.bonus_points,
        "grading_instructions": format_grading_instructions(exercise.grading_instructions, exercise.grading_criteria),
        "problem_statement": exercise.problem_statement or "No problem statement.",
        "example_solution": exercise.example_solution,
        "submission": add_sentence_numbers(submission.text)
    }

    chat_prompt = get_chat_prompt_with_formatting_instructions(
        model=model, 
        system_message=config.generate_suggestions_prompt.system_message, 
        human_message=config.generate_suggestions_prompt.human_message, 
        pydantic_object=AssessmentModel
    )

    # Check if the prompt is too long and omit features if necessary (in order of importance)
    omittable_features = ["example_solution", "problem_statement", "grading_instructions"]
    prompt_input, should_run = check_prompt_length_and_omit_features_if_necessary(
        prompt=chat_prompt,
        prompt_input= prompt_input,
        max_input_tokens=config.max_input_tokens,
        omittable_features=omittable_features,
        debug=debug
    )

    # Skip if the prompt is too long
    if not should_run:
        logger.warning("Input too long. Skipping.")
        if debug:
            emit_meta("prompt", chat_prompt.format(**prompt_input))
            emit_meta("error", f"Input too long {num_tokens_from_prompt(chat_prompt, prompt_input)} > {config.max_input_tokens}")
        return []

    result = await predict_and_parse(
        model=model, 
        chat_prompt=chat_prompt, 
        prompt_input=prompt_input, 
        pydantic_object=AssessmentModel,
        tags=[
            f"exercise-{exercise.id}",
            f"submission-{submission.id}",
        ]
    )

    if debug:
        emit_meta("generate_suggestions", {
            "prompt": chat_prompt.format(**prompt_input),
            "result": result.dict() if result is not None else None
        })

    if result is None:
        return []

    grading_instruction_ids = set(
        grading_instruction.id 
        for criterion in exercise.grading_criteria or [] 
        for grading_instruction in criterion.structured_grading_instructions
    )

    feedbacks = []
    for feedback in result.feedbacks:
        index_start, index_end = get_index_range_from_line_range(feedback.line_start, feedback.line_end, submission.text)
        grading_instruction_id = feedback.grading_instruction_id if feedback.grading_instruction_id in grading_instruction_ids else None
        feedbacks.append(Feedback(
            exercise_id=exercise.id,
            submission_id=submission.id,
            title=feedback.title,
            description=feedback.description,
            index_start=index_start,
            index_end=index_end,
            credits=feedback.credits,
            structured_grading_instruction_id=grading_instruction_id,
            meta={}
        ))

    return feedbacks