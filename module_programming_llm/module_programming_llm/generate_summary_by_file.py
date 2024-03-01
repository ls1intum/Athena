import asyncio
from typing import Optional, Sequence, List, Dict
from collections import defaultdict

from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate

from athena import emit_meta
from athena.programming import Exercise, Submission

from module_programming_llm.config import GradedBasicApproachConfig, BasicApproachConfig
from module_programming_llm.helpers.llm_utils import (
    get_chat_prompt_with_formatting_instructions,
    num_tokens_from_prompt,
    predict_and_parse
)
from module_programming_llm.helpers.utils import load_files_from_repo, add_line_numbers


class FileDescription(BaseModel):
    file_name: str = Field(description="File name")
    description: str = Field(description="Summary relevant for this file")

    class Config:
        title = "FileDescription"


class SolutionSummary(BaseModel):
    """Collection of summaries, accessible by file path"""
    items: Dict[str, str] = Field(description="File summaries indexed by file path")

    class Config:
        title = "SolutionSummary"

    def describe_solution_summary(self) -> str:
        descriptions = []
        for file_path, file_summary in self.items.items():
            description = f"File {file_path}: {file_summary}"
            descriptions.append(description)
        return "\n".join(descriptions)


# pylint: disable=too-many-locals
async def generate_summary_by_file(
        exercise: Exercise,
        submission: Submission,
        prompt: ChatPromptTemplate,
        config: BasicApproachConfig,
        debug: bool
) -> Optional[SolutionSummary]:
    """Generaty summary for the submission file by file

    Args:
        exercise (Exercise): Exercise to split the problem statement for (respecting the changed files)
        submission (Submission): Submission to split the problem statement for (respecting the changed files)
        prompt (ChatPromptTemplate): Prompt template to check for problem_statement
        config (GradedBasicApproachConfig): Configuration

    Returns:
        Optional[SolutionSummary]: Summarization of the given submission, None if it is too short or too long
    """

    # Return None if submission_file not in the prompt
    if "summary" not in prompt.input_variables:
        return None

    model = config.model.get_model()  # type: ignore[attr-defined]

    submission_repo = submission.get_repository()

    files = load_files_from_repo(submission_repo)

    chat_prompt = get_chat_prompt_with_formatting_instructions(
        model=model,
        system_message=config.generate_file_summary_prompt.system_message,
        human_message=config.generate_file_summary_prompt.human_message,
        pydantic_object=FileDescription
    )

    prompt_inputs = []

    # Gather prompt inputs for each file (independently)
    for file_path, file_content in files.items():
        file_content = add_line_numbers(file_content)

        prompt_inputs.append({
            "submission_file": file_content,
            "file_path": file_path,
        })

    valid_prompt_inputs = [
        prompt_input for prompt_input in prompt_inputs
        if num_tokens_from_prompt(chat_prompt, prompt_input) <= config.max_input_tokens
    ]

    # noinspection PyTypeChecker
    results: List[Optional[FileDescription]] = await asyncio.gather(*[
        predict_and_parse(
            model=model,
            chat_prompt=chat_prompt,
            prompt_input=prompt_input,
            pydantic_object=FileDescription,
            tags=[
                f"exercise-{exercise.id}",
                f"submission-{submission.id}",
                f"file-{prompt_input['file_path']}",
                "generate-summary-by-file"
            ]
        ) for prompt_input in valid_prompt_inputs
    ])

    if debug:
        for prompt_input, result in zip(valid_prompt_inputs, results):
            emit_meta("file_summary", {
                "prompt": chat_prompt.format(**prompt_input),
                "result": result.dict() if result is not None else None,
                "file_path": prompt_input['file_path']  # Include the file path for reference
            })

    if not any(result is not None for result in results):
        return None

    items_dict = {}

    for _, file_summary in enumerate(results):
        if file_summary is not None:
            items_dict[file_summary.file_name] = file_summary.description

    return SolutionSummary(items=items_dict)
