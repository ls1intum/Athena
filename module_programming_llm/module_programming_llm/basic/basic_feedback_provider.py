from typing import List

import git

from athena import Feedback, ProgrammingExercise, Submission
from athena.helpers import get_repositories

from langchain.chat_models import PromptLayerChatOpenAI
from langchain.schema import HumanMessage

from ..feedback_provider_registry import register_feedback_provider


@register_feedback_provider("basic")
def suggest_feedback(exercise: ProgrammingExercise, submission: Submission) -> List[Feedback]:
    chat = PromptLayerChatOpenAI(pl_tags=["basic"])
    
    with get_repositories(urls=[ submission.content]) as repositories:
        submission = repositories
# solution, template,
# exercise.solution_repository_url, exercise.template_repository_url,
        print(submission)


        # output = chat([HumanMessage(content="I am a cat and I want")])
    # print(output)
    return []