from typing import List

import git

from athena import Feedback, ProgrammingExercise, Submission
from athena.helpers import get_repositories

from langchain.chat_models import PromptLayerChatOpenAI
from langchain.schema import HumanMessage

from ..helpers.utils import get_diff, merge_repos_by_filepath, add_line_numbers

from ..feedback_provider_registry import register_feedback_provider


@register_feedback_provider("basic")
def suggest_feedback(exercise: ProgrammingExercise, submission: Submission) -> List[Feedback]:
    chat = PromptLayerChatOpenAI(pl_tags=["basic"])
    
    with get_repositories(exercise.solution_repository_url, exercise.template_repository_url, submission.content) as repositories:
        solution_repo, template_repo, submission_repo = repositories
        for file_path, contents in merge_repos_by_filepath(*repositories, file_filter=lambda x: x.endswith(".java")): # TODO file_filter
            solution, template, submission = contents
            if submission is None:
                continue

            print(get_diff(src_repo=solution_repo,
                           dst_repo=submission_repo,
                           src_prefix="solution",
                           dst_prefix="submission",
                           file_path=file_path))
            print(get_diff(src_repo=submission_repo,
                           dst_repo=solution_repo,
                           src_prefix="submission",
                           dst_prefix="solution",
                           file_path=file_path))
            
            # print(get_diff(src_repo=solution_repo, dst_repo=submission_repo, file_path=file_path))

            # diff = get_diff(solution, submission, file_path=file_path)
            # print(diff)

        # output = chat([HumanMessage(content="I am a cat and I want")])
    # print(output)
    return []