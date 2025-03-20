from abc import ABC

from pydantic import BaseModel, Field

from llm_core.models import ModelConfigType, DefaultModelConfig
from athena import config_schema_provider
from module_programming_llm.prompts import SplitProblemStatementByFile, SplitGradingInstructionsByFile, \
    GenerateSuggestionsByFile, GenerateFileSummary, GenerateSuggestionsZeroShot
from module_programming_llm.prompts.filter_out_solution.filter_out_solution_by_file import FilterOutSolutionByFile
from module_programming_llm.prompts.filter_out_solution.filter_out_solution_zero_shot import FilterOutSolutionZeroShot
from module_programming_llm.prompts.generate_grading_criterion.generate_grading_criterion import \
    GenerateGradingCriterion
from module_programming_llm.prompts.rag import RAG


class BasicApproachConfig(BaseModel):
    """Defines a basic configuration for processing submissions, incorporating problem statement splitting, feedback generation."""

    max_input_tokens: int = Field(default=5000, description="Maximum number of tokens in the input prompt.")
    model: ModelConfigType = Field(default=DefaultModelConfig())  # type: ignore


class BasicByFileApproachConfig(BasicApproachConfig, ABC):
    """
    This approach uses an LLM to split up the problem statement and grading instructions by file, if necessary.
    Then, it generates graded suggestions for each file independently.
    Generates grading instructions if not available.
    Validates generated feedback.
    """

    split_problem_statement_by_file: SplitProblemStatementByFile = Field(default=SplitProblemStatementByFile())
    split_grading_instructions_by_file: SplitGradingInstructionsByFile = (
        Field(default=SplitGradingInstructionsByFile()))
    generate_suggestions_by_file: GenerateSuggestionsByFile = Field(default=GenerateSuggestionsByFile())
    generate_file_summary: GenerateFileSummary = Field(default=GenerateFileSummary())
    filter_out_solution: FilterOutSolutionByFile = Field(default=FilterOutSolutionByFile())
    generate_grading_criterion: GenerateGradingCriterion = Field(default=GenerateGradingCriterion())
    max_number_of_files: int = Field(default=25,
                                     description="Maximum number of files. If exceeded, it will prioritize the most important submitted files.")
    tokens_before_split: int = Field(default=1000,
                                     description="Split the prompt into file-based ones after this number of tokens.")
    rag_requests: RAG = Field(default=RAG())


class ZeroShotApproachConfig(BasicApproachConfig, ABC):
    """
    This approach uses an LLM to generate graded suggestions for the whole submission jointly.
    Generates grading instructions if not available.
    Validates generated feedback.
    """
    generate_suggestions_zero_shot: GenerateSuggestionsZeroShot = Field(default=GenerateSuggestionsZeroShot())
    filter_out_solution: FilterOutSolutionZeroShot = Field(default=FilterOutSolutionZeroShot())
    generate_grading_criterion: GenerateGradingCriterion = Field(default=GenerateGradingCriterion())
    rag_requests: RAG = Field(default=RAG())


@config_schema_provider
class Configuration(BaseModel):
    """Configuration settings for the entire module, including debug mode and approach-specific configurations."""

    debug: bool = Field(default=False, description="Enable debug mode.")
    basic_by_file_approach: BasicByFileApproachConfig = Field(default=BasicByFileApproachConfig())
    zero_shot_approach: ZeroShotApproachConfig = Field(default=ZeroShotApproachConfig())
