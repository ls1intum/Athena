
from typing import List, Optional, Sequence
from pydantic import BaseModel, Field

from athena.text import Exercise, Submission, Feedback
from module_text_llm.config import BasicApproachConfig, ChainOfThoughtConfig


from module_text_llm.approaches.basic_approach.generate_suggestions import generate_suggestions as generate_suggestions_basic
from module_text_llm.approaches.chain_of_thought_approach.generate_suggestions import generate_suggestions as generate_cot_suggestions

async def generate_suggestions(exercise: Exercise, submission: Submission, config: BasicApproachConfig, debug: bool) -> List[Feedback]:
    if(isinstance(config, BasicApproachConfig)):
        return await generate_suggestions_basic(exercise, submission, config, debug)
    elif(isinstance(config, ChainOfThoughtConfig)):
        return await generate_cot_suggestions(exercise, submission, config, debug)
