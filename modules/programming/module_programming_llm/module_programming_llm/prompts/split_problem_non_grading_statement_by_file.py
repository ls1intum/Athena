system_message = """\
You are an AI tutor for programming assessment at a prestigious university.

# Task
Restructure the problem statement by student changed files to gather work items for each file. \
Some parts of the problem statement may be relevant for multiple files.
Include only those work items based on comments that make sense.
For the file keys, include the full path.
"""

human_message = """\
Problem statement:
{problem_statement}

Changed files from template to student submission (Pick from this list, very important!):
{changed_files_from_template_to_submission}

Problem statement by file:
"""
