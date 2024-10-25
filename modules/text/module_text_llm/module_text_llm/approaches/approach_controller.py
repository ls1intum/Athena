
from typing import List
from athena.text import Exercise, Submission, Feedback
from module_text_llm.approaches.basic_approach.config import BasicApproachConfig
from module_text_llm.approaches.chain_of_thought_approach.config  import ChainOfThoughtConfig
from module_text_llm.approaches.approach_config import ApproachConfig
from athena.logger import logger


from module_text_llm.approaches.basic_approach.generate_suggestions import generate_suggestions as generate_suggestions_basic
from module_text_llm.approaches.chain_of_thought_approach.generate_suggestions import generate_suggestions as generate_cot_suggestions

async def generate_suggestions(exercise: Exercise, submission: Submission, config: ApproachConfig, debug: bool) -> List[Feedback]:
    if(isinstance(config, BasicApproachConfig)):
        return await generate_suggestions_basic(exercise, submission, config, debug)
    elif(isinstance(config, ChainOfThoughtConfig)):
        return await generate_cot_suggestions(exercise, submission, config, debug)

