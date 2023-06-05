import json
from typing import List

from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from athena.programming import Exercise, Submission, Feedback
from athena.logger import logger

from module_programming_llm.helpers.utils import get_diff, get_file_extension, load_files_from_repo, add_line_numbers
from module_programming_llm.helpers.models import chat

async def suggest_feedback(exercise: Exercise, submission: Submission) -> List[Feedback]:
    max_prompt_length = 2560
    input_list: List[dict] = []

    if exercise.meta['file_grading_instructions'] is None:
        raise ValueError("No file grading instructions found for exercise in meta.")
    if exercise.meta['file_problem_statements'] is None:
        raise ValueError("No file problem statements found for exercise in meta.")

    # Feature extraction
    solution_repo = exercise.get_solution_repository()
    template_repo = exercise.get_template_repository()
    submission_repo = submission.get_repository()
    
    file_extension = get_file_extension(exercise.programming_language)
    if file_extension is None:
        raise ValueError(f"Could not determine file extension for programming language {exercise.programming_language}.")

    for file_path, submission_content in load_files_from_repo(submission_repo, file_filter=lambda x: x.endswith(file_extension)).items():
        if submission_content is None:
            continue
            
        problem_statement = exercise.meta['file_problem_statements'][file_path]
        if problem_statement is None:
            logger.info("No problem statement for %s, skipping.", file_path)
            continue

        grading_instructions = exercise.meta['file_grading_instructions'][file_path]
        if grading_instructions is None:
            logger.info("No grading instructions for %s, skipping.", file_path)
            continue

        submission_content = add_line_numbers(submission_content)
        solution_to_submission_diff = get_diff(src_repo=solution_repo, dst_repo=submission_repo, src_prefix="solution", dst_prefix="submission", file_path=file_path)
        template_to_submission_diff = get_diff(src_repo=template_repo, dst_repo=submission_repo, src_prefix="template", dst_prefix="submission", file_path=file_path)

        input_list.append({
            "file_path": file_path,
            "submission_content": submission_content,
            "solution_to_submission_diff": solution_to_submission_diff,
            "template_to_submission_diff": template_to_submission_diff,
            "grading_instructions": grading_instructions,
            "problem_statement": problem_statement,
        })

    # Prompt building
    system_template = """\
You are a programming tutor AI at a university tasked with grading and providing feedback to programming homework assignments.

You receive a submission with some other information and respond with the following JSON format:
[{{"text": <feedback_comment>, "credits": <number>, "line": <nullable line number (no range)>}}]
Extremely Important: The response should only contain the json object with the feedback, nothing else!

Effective feedback for programming assignments should possess the following qualities:
1. Constructive: Provide guidance on how to improve the code, pointing out areas that can be optimized, refactored, or enhanced.
2. Specific: Highlight exact lines or sections of code that need attention, and suggest precise changes or improvements.
3. Balanced: Recognize and praise the positive aspects of the code, while also addressing areas for improvement, to encourage and motivate the student.
4. Clear and concise: Use straightforward language and avoid overly technical jargon, so that the student can easily understand the feedback.
5. Actionable: Offer practical suggestions for how the student can apply the feedback to improve their code, ensuring they have a clear path forward.
6. Educational: Explain the reasoning behind the suggestions, so the student can learn from the feedback and develop their programming skills.

Example response:
[\
{{"text": "Great use of the compareTo method for comparing Dates, which is the proper way to compare objects.", "credits": 3, "line": 14}},\
{{"text": "Good job implementing the BubbleSort algorithm for sorting Dates. It shows a clear understanding of the sorting process", "credits": 5, "line": null}},\
{{"text": "Incorrect use of \'==\' for string comparison, which leads to unexpected results. Use the \'equals\' method for string comparison instead.", "credits": -2, "line": 18}}\
]\
"""
    human_template = """\
Student\'s submission to grade:
{submission_content}
Diff between solution (deletions) and student\'s submission (additions):
{solution_to_submission_diff}
Diff between template (deletions) and student\'s submission (additions):
{template_to_submission_diff}
Problem statement:
{problem_statement}
Grading instructions:
{grading_instructions}
As said, it should be effective feedback following an extremely high standard.
Critically grade the submission and distribute credits accordingly.
Be liberal with interpreting the grading instructions.

JSON response:
"""
    
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # Filter long prompts
    input_list = [input for input in input_list if chat.get_num_tokens_from_messages(chat_prompt.format_messages(**input)) <= max_prompt_length]

    # Completion
    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = await chain.agenerate(input_list)
    
    # Parse result
    feedback_proposals: List[Feedback] = []
    for input, generations in zip(input_list, result.generations):
        file_path = input["file_path"]
        for generation in generations:
            try:
                feedbacks = json.loads(generation.text)
            except json.JSONDecodeError:
                logger.error("Failed to parse feedback json:", generation.text)
                continue
            if not isinstance(feedbacks, list):
                logger.error("Feedback json is not a list:", generation.text)
                continue

            for feedback in feedbacks:
                line = feedback.get("line", None)
                detail_text = feedback.get("text", "")
                credits = feedback.get("credits", 0.0)
                feedback_proposals.append(
                    Feedback(
                        exercise_id=exercise.id,
                        submission_id=submission.id,
                        detail_text=detail_text,
                        file_path=file_path,
                        line=line,
                        credits=credits,
                        meta={},
                    )
                )

    return feedback_proposals