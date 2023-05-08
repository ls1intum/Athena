import json

from athena import ProgrammingExercise
from athena.helpers import get_repositories

from module_programming_llm.helpers.utils import get_diff

from langchain.chains import LLMChain
from langchain.chat_models import PromptLayerChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

def generate_file_grading_instructions(exercise: ProgrammingExercise):
    chat = PromptLayerChatOpenAI(pl_tags=["grading_instructions", "file_grading_instructions"], temperature=0)
    grading_instructions = exercise.grading_instructions

    with get_repositories(exercise.solution_repository_url, exercise.template_repository_url) as repositories:
        solution_repo, template_repo = repositories
        changed_files = get_diff(src_repo=template_repo, dst_repo=solution_repo, file_path="*.java", name_only=True)
        
    system_template = (
        'You are a programming tutor AI at a university tasked with grading and providing feedback to programming homework assignments.\n'
        '\n'
        'You receive grading instructions and a list of changed files and respond in the following JSON format, associating each file with its grading instructions:\n'
        '{{"<filename>": "<file grading instructions>"}}\n'
    )
    human_template = (
        'Grading instructions:\n'
        '{grading_instructions}\n'
        'Changed files:\n'
        '{changed_files}\n'
        '\n'
        'JSON response:\n'
    )
    
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    result = chat(chat_prompt.format_prompt(grading_instructions=grading_instructions, changed_files=changed_files).to_messages())
    
    try:
        return json.loads(result.content)
    except json.JSONDecodeError:
        print("Could not decode JSON response from chatbot:")
        print(result.content)
    return None

def generate_file_problem_statements(exercise: ProgrammingExercise):
    chat = PromptLayerChatOpenAI(pl_tags=["problem_statement", "file_problem_statement"], temperature=0)
    problem_statement = exercise.problem_statement

    with get_repositories(exercise.solution_repository_url, exercise.template_repository_url) as repositories:
        solution_repo, template_repo = repositories
        changed_files = get_diff(src_repo=template_repo, dst_repo=solution_repo, file_path="*.java", name_only=True)
        
    system_template = (
        'You are a programming tutor AI at a university tasked with grading and providing feedback to programming homework assignments.\n'
        '\n'
        'You receive a overall problem statement and a list of changed files and respond in the following JSON format, associating each file with its file-specific problem statement:\n'
        '{{"<filename>": "<file problem statement>"}}\n'
    )
    human_template = (
        'Problem statement:\n'
        '{problem_statement}\n'
        'Changed files:\n'
        '{changed_files}\n'
        '\n'
        'JSON response:\n'
    )
    
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    result = chat(chat_prompt.format_prompt(problem_statement=problem_statement, changed_files=changed_files).to_messages())
    
    try:
        return json.loads(result.content)
    except json.JSONDecodeError:
        print("Could not decode JSON response from chatbot:")
        print(result.content)
    return None