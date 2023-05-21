import json

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from athena.programming import Exercise

from module_programming_llm.helpers.utils import get_diff, get_file_extension
from module_programming_llm.helpers.models import chat

def generate_file_grading_instructions(exercise: Exercise):
    grading_instructions = exercise.grading_instructions

    solution_repo = exercise.get_solution_repository()
    template_repo = exercise.get_template_repository()
    file_extension = get_file_extension(exercise.programming_language) or ""
    changed_files = get_diff(src_repo=template_repo, dst_repo=solution_repo, file_path=f"*{file_extension}", name_only=True)
    
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


def generate_file_problem_statements(exercise: Exercise):
    problem_statement = exercise.problem_statement

    solution_repo = exercise.get_solution_repository()
    template_repo = exercise.get_template_repository()
    file_extension = get_file_extension(exercise.programming_language) or ""
    changed_files = get_diff(src_repo=template_repo, dst_repo=solution_repo, file_path=f"*{file_extension}", name_only=True)
        
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