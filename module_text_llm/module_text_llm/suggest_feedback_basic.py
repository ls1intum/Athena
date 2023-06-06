from typing import List

from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from athena.text import Exercise, Submission, Feedback
from athena.logger import logger

from module_text_llm.helpers.models import chat

from .prompts.suggest_feedback import system_template, human_template

async def suggest_feedback_basic(exercise: Exercise, submission: Submission) -> List[Feedback]:
    return []