from typing import Optional

from athena.programming import Submission, Feedback
from module_programming_ast.convert_code_to_ast.antlr_to_apted_tree import parse_python_file, parse_java_file
from module_programming_ast.convert_code_to_ast.method_node import MethodNode
from athena.logger import logger


def get_feedback_method(submission: Submission, feedback: Feedback, programming_language: str) -> Optional[MethodNode]:
    """Find method that the feedback is on"""
    if feedback.file_path is None or feedback.line_start is None:
        return None
    try:
        code = submission.get_code(feedback.file_path)
    except UnicodeDecodeError:
        logger.warning("File %s in submission %d is not UTF-8 encoded.", feedback.file_path, submission.id)
        return None
    if programming_language == "java":
        methods = parse_java_file(code)
    elif programming_language == "python":
        methods = parse_python_file(code)
    else:
        logger.warning("Unsupported programming language.")
        return None
    for m in methods:
        if m.line_start is None or m.line_end is None:
            continue
        # method has to contain all feedback lines
        if m.line_start <= feedback.line_start:
            feedback_line_end = feedback.line_end if feedback.line_end is not None else feedback.line_start
            if m.line_end >= feedback_line_end:
                return m
    return None
