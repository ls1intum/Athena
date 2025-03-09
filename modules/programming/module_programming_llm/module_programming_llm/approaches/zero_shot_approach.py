from typing import Optional, List

from athena.programming import Submission, Exercise, Feedback
from module_programming_llm.config import Configuration
from llm_core.models import ModelConfigType
from module_programming_llm.helpers import bulk_search
from module_programming_llm.prompts import GenerateSuggestionsZeroShot, FilterOutSolutionZeroShot
from module_programming_llm.prompts.filter_out_solution.filter_out_solution_input import FilterOutSolutionInput
from module_programming_llm.prompts.filter_out_solution.filter_out_solution_output import FilterOutSolutionOutput
from module_programming_llm.prompts.generate_grading_criterion.generate_grading_criterion import \
    GenerateGradingCriterion, GenerateGradingCriterionOutput, GenerateGradingCriterionInput
from module_programming_llm.prompts.generate_suggestions import \
    GenerateSuggestionsInput, GenerateSuggestionsOutput
from module_programming_llm.prompts.rag import RAGInput, RAG, RAGOutput


async def generate_suggestions(step: GenerateSuggestionsZeroShot,
                               input_data: GenerateSuggestionsInput, debug: bool,
                               model: ModelConfigType) -> List[Optional[GenerateSuggestionsOutput]]:  # type: ignore
    return await step.process(input_data, debug, model)


async def filter_out_solutions(step: FilterOutSolutionZeroShot,
                               input_data: FilterOutSolutionInput, debug: bool,
                               model: ModelConfigType) -> List[Optional[FilterOutSolutionOutput]]:  # type: ignore
    return await step.process(input_data, debug, model)


async def generate_grading_criterion(step: GenerateGradingCriterion,
                                     input_data: GenerateGradingCriterionInput, debug: bool,
                                     model: ModelConfigType) -> Optional[GenerateGradingCriterionOutput]:  # type: ignore
    return await step.process(input_data, debug, model)


async def generate_rag_queries(step: RAG,
                                     input_data: RAGInput, debug: bool,
                                     model: ModelConfigType) -> Optional[RAGOutput]:  # type: ignore
    return await step.process(input_data, debug, model)


async def generate_feedback(exercise: Exercise, submission: Submission, is_graded: bool,
                            module_config: Configuration) -> List[Feedback]:  # type: ignore
    template_repo = exercise.get_template_repository()
    solution_repo = exercise.get_solution_repository()
    submission_repo = submission.get_repository()
    is_debug = module_config.debug
    model = module_config.zero_shot_approach.model

    rag_query_input = RAGInput(template_repo, solution_repo, exercise.id, exercise.problem_statement)
    rag_query_output = await generate_rag_queries(module_config.zero_shot_approach.rag_requests, rag_query_input, module_config.debug, model)

    rag_result = [] if rag_query_output is None else bulk_search(rag_query_output.rag_queries, model)

    if not exercise.grading_criteria:
        generate_grading_criterion_input = GenerateGradingCriterionInput(template_repo, solution_repo, exercise.id,
                                                                         exercise.max_points, exercise.bonus_points,
                                                                         exercise.problem_statement,
                                                                         exercise.grading_instructions)
        generate_grading_criterion_output = await generate_grading_criterion(
            module_config.zero_shot_approach.generate_grading_criterion, generate_grading_criterion_input, is_debug,
            model)
        if generate_grading_criterion_output is not None:
            exercise.grading_criteria = generate_grading_criterion_output.structured_grading_criterion.criteria

    generate_suggestions_input = GenerateSuggestionsInput(template_repo, submission_repo, solution_repo,
                                                                exercise.id,
                                                                submission.id, exercise.max_points,
                                                                exercise.bonus_points, exercise.programming_language,
                                                                "",
                                                                rag_result,
                                                                None,
                                                                None,
                                                                exercise.grading_criteria, exercise.problem_statement,
                                                                exercise.grading_instructions)
    output = await generate_suggestions(
        module_config.zero_shot_approach.generate_suggestions_zero_shot, generate_suggestions_input, is_debug, model)

    if not is_graded:
        filter_out_solution_input = FilterOutSolutionInput(solution_repo, template_repo, exercise.problem_statement,
                                                           exercise.id, submission.id, output,
                                                           None)
        output = await filter_out_solutions(module_config.zero_shot_approach.filter_out_solution,
                                            filter_out_solution_input, is_debug, model)

    grading_instruction_ids = set(
        grading_instruction.id
        for criterion in exercise.grading_criteria or []
        for grading_instruction in criterion.structured_grading_instructions
    )

    feedbacks: List[Feedback] = []
    for result in output:
        if result is None:
            continue
        for feedback in result.feedbacks:
            grading_instruction_id = (
                feedback.grading_instruction_id
                if feedback.grading_instruction_id in grading_instruction_ids
                else None
            )
            feedbacks.append(
                Feedback(
                    exercise_id=exercise.id,
                    submission_id=submission.id,
                    title=feedback.title,
                    description=feedback.description,
                    file_path=result.file_path,
                    line_start=feedback.line_start,
                    line_end=feedback.line_end,
                    credits=feedback.credits,
                    structured_grading_instruction_id=grading_instruction_id,
                    is_graded=is_graded,
                    meta={},
                )
            )

    return feedbacks
