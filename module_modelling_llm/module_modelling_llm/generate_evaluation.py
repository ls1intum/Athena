import json
from typing import List, Sequence, Dict, Literal

from pydantic import BaseModel, Field

from athena.logger import logger
from athena.modelling import Exercise, Submission, Feedback
from module_modelling_llm.helpers.llm_utils import (
    get_chat_prompt_with_formatting_instructions,
    check_prompt_length_and_omit_features_if_necessary,
    predict_and_parse
)
from module_modelling_llm.helpers.models import evaluation_model
from module_modelling_llm.helpers.serializers.diagram_model_serializer import DiagramModelSerializer
from module_modelling_llm.prompts.generate_evaluation import system_message, human_message


class AccuracyMetric(BaseModel):
    id: int = Field(..., description="Feedback ID")
    reasoning: str = Field(..., description="Step-by-step critical reasoning of the labels")
    acceptance_label: Literal["accepted", "rejected"] = Field(..., description="Estimated acceptance label")
    level_of_needed_modification_label: Literal["no", "minor", "major"] = Field(...,
                                                                                description="Estimated level of needed modification")


class Evaluation(BaseModel):
    metrics: Sequence[AccuracyMetric] = Field(...)


async def generate_evaluation(
        exercise: Exercise,
        submission: Submission,
        true_feedbacks: List[Feedback],
        predicted_feedbacks: List[Feedback]
) -> Dict[int, dict]:
    if evaluation_model is None:
        raise EnvironmentError("No evaluation model available, please set up LLM_EVALUATION_MODEL correctly"
                               "by setting it to one of the available models logged during startup.")
    max_input_tokens = 3000

    def feedback_to_dict(feedback: Feedback):
        return {
            "id": feedback.id,
            "title": feedback.title,
            "description": feedback.description,
            "credits": feedback.credits
        }

    submission_diagram = json.loads(submission.model)
    serialized_submission = DiagramModelSerializer.serialize_model(submission_diagram)

    prompt_input = {
        "submission": serialized_submission,
        "true_feedbacks": json.dumps([feedback_to_dict(feedback) for feedback in true_feedbacks]),
        "predicted_feedbacks": json.dumps([feedback_to_dict(feedback) for feedback in predicted_feedbacks]),
    }

    chat_prompt = get_chat_prompt_with_formatting_instructions(
        model=evaluation_model,
        system_message=system_message,
        human_message=human_message,
        pydantic_object=Evaluation
    )

    # Check if the prompt is too long and omit features if necessary (in order of importance)
    omittable_features = ["submission"]
    prompt_input, should_run = check_prompt_length_and_omit_features_if_necessary(
        prompt=chat_prompt,
        prompt_input=prompt_input,
        max_input_tokens=max_input_tokens,
        omittable_features=omittable_features,
        debug=False
    )

    if not should_run:
        logger.warning("Evaluation input too long. Skipping.")
        return {}

    result = await predict_and_parse(
        model=evaluation_model,
        chat_prompt=chat_prompt,
        prompt_input=prompt_input,
        pydantic_object=Evaluation,
        tags=[
            f"exercise-{exercise.id}",
            f"submission-{submission.id}",
            "evaluation"
        ]
    )

    if result is None:
        logger.warning("Evaluation failed. Skipping.")
        return {}

    return {item.id: item.dict() for item in result.metrics}
