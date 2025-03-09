import asyncio
import os
from typing import Optional, List

from athena import emit_meta
from module_programming_llm.prompts.pipeline_step import PipelineStep
from .. import GenerateSuggestionsInput
from ..generate_suggestions_output import GenerateSuggestionsOutput
from prompt import system_message as prompt_system_message, human_message as prompt_human_message
from pydantic import Field
from llm_core.utils.llm_utils import (
    get_chat_prompt_with_formatting_instructions,
    check_prompt_length_and_omit_features_if_necessary,
)
from llm_core.utils.predict_and_parse import predict_and_parse
from module_programming_llm.helpers.utils import (
    get_diff,
    load_files_from_repo,
    add_line_numbers, format_grading_instructions
)
from llm_core.models import ModelConfigType


class GenerateSuggestionsZeroShot(PipelineStep[GenerateSuggestionsInput, List[Optional[GenerateSuggestionsOutput]]]):
    """Generates concise feedback for submitted files, facilitating a quicker review and understanding of the content"""

    system_message: str = Field(prompt_system_message,
                                description="Message for priming AI behavior and instructing it what to do.")
    human_message: str = Field(prompt_human_message,
                               description="Message from a human. The input on which the AI is supposed to act.")

    # pylint: disable=too-many-locals
    async def process(self, input_data: GenerateSuggestionsInput, debug: bool, model: ModelConfigType) -> List[
        Optional[GenerateSuggestionsOutput]]:  # type: ignore
        model = model.get_model()  # type: ignore[attr-defined]

        prompt = get_chat_prompt_with_formatting_instructions(
            model=model,
            system_message=self.system_message,
            human_message=self.human_message,
            pydantic_object=GenerateSuggestionsOutput,
        )

        solution_repo = input_data.solution_repo
        template_repo = input_data.template_repo
        submission_repo = input_data.submission_repo

        changed_files_from_template_to_submission = get_diff(
            src_repo=template_repo, dst_repo=submission_repo, file_path=None, name_only=True
        ).split("\n")
        changed_files_from_template_to_submission = [
            os.path.join(str(submission_repo.working_tree_dir or ""), file_path)
            for file_path in changed_files_from_template_to_submission
        ]

        # Changed text files
        changed_files = load_files_from_repo(
            submission_repo,
            file_filter=lambda file_path: file_path in changed_files_from_template_to_submission,
        )

        problem_statement = (
            input_data.problem_statement
            if input_data.problem_statement.strip()
            else "No problem statement found."
        )

        grading_instructions = format_grading_instructions(input_data.grading_instructions,
                                                           input_data.grading_criteria) or ""
        grading_instructions = (
            grading_instructions
            if grading_instructions.strip()
            else "No grading instructions found."
        )
        submission_files = ""
        template_to_submission_files = ""
        template_to_solution_files = ""

        # Just concatenate all changed files into one string object
        # The LLM will process them jointly here
        for file_path, file_content in changed_files.items():
            file_content = add_line_numbers(file_content)
            submission_files += "File path: {0}\nFile content: {1}\n".format(file_path, file_content)

            template_to_submission_diff = get_diff(
                src_repo=template_repo,
                dst_repo=submission_repo,
                src_prefix="template",
                dst_prefix="submission",
                file_path=file_path,
            )
            template_to_submission_files += "File path: {0}\nFile content: {1}\n".format(file_path,
                                                                                         template_to_submission_diff)

            template_to_solution_diff = get_diff(
                src_repo=template_repo,
                dst_repo=solution_repo,
                src_prefix="template",
                dst_prefix="solution",
                file_path=file_path,
            )
            template_to_solution_files += "File path: {0}\nFile content: {1}\n".format(file_path,
                                                                                       template_to_solution_diff)

        prompt_input = {
            "max_points": input_data.max_points,
            "bonus_points": input_data.bonus_points,
            "template_to_submission_diff": template_to_submission_files,
            "template_to_solution_diff": template_to_solution_files,
            "grading_instructions": grading_instructions,
            "problem_statement": problem_statement,
            "rag_data": input_data.rag_data,
            "submission_files": submission_files
        }

        # Filter long prompts (omitting features if necessary)
        # Lowest priority features are at the top of the list (i.e. they are omitted first if necessary)
        # "submission_files" is not omittable, because it is the main input containing the line numbers
        # In the future we might be able to include the line numbers in the diff, but for now we need to keep it
        omittable_features = [
            "template_to_solution_diff",
            # If it is even included in the prompt (has the lowest priority since it is indirectly included in other diffs)
            "problem_statement",
            "grading_instructions",
            "solution_to_submission_diff",
            "template_to_submission_diff"
            # In the future we might indicate the changed lines in the submission_file additionally
        ]

        prompt_inputs = [
            omitted_prompt_input
            for omitted_prompt_input, should_run in [
                check_prompt_length_and_omit_features_if_necessary(
                    prompt=prompt,
                    prompt_input=prompt_input,
                    max_input_tokens=self.max_input_tokens,
                    omittable_features=omittable_features,
                    debug=debug,
                )
            ]
            if should_run
        ]

        # noinspection PyTypeChecker
        results: List[Optional[GenerateSuggestionsOutput]] = await asyncio.gather(
            *[
                predict_and_parse(
                    model=model,
                    chat_prompt=prompt,
                    prompt_input=prompt_input,
                    pydantic_object=GenerateSuggestionsOutput,
                    tags=[
                        f"exercise-{input_data.exercise_id}",
                        f"submission-{input_data.submission_id}",
                        "generate-suggestions-zero-shot",
                    ],
                )
                for prompt_input in prompt_inputs
            ]
        )

        if debug:
            emit_meta(
                "generate_suggestions_zero_shot",
                [
                    {
                        "prompt": prompt.format(**prompt_input),
                        "result": result.dict() if result is not None else None,
                    }
                    for prompt_input, result in zip(prompt_inputs, results)
                ],
            )

        return results
