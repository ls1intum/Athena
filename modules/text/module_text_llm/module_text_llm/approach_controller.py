
from typing import List, Optional, Sequence
from pydantic import BaseModel, Field

from athena import emit_meta
from athena.text import Exercise, Submission, Feedback
from athena.logger import logger
from module_text_llm.config import BasicApproachConfig, ChainOfThoughtConfig


from module_text_llm.helpers.utils import add_sentence_numbers, get_index_range_from_line_range, format_grading_instructions
from module_text_llm.generate_suggestions import generate_suggestions
from module_text_llm.generate_cot_suggestions import generate_cot_suggestions

async def generate(exercise: Exercise, submission: Submission, config: BasicApproachConfig, debug: bool) -> List[Feedback]:
    if(isinstance(config, BasicApproachConfig)):
        return await generate_suggestions(exercise, submission, config, debug)
    elif(isinstance(config, ChainOfThoughtConfig)):
        return await generate_cot_suggestions(exercise, submission, config, debug)
