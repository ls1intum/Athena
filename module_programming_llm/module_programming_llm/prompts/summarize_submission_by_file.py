system_message = """\
# Task
Create a global short description for the following code file. 
In the next steps you will be given files one by one and be asked to create code review for them.
By doing so the global structure is lost.
Your output should help you in the future to create precise feedback.
For file path keys include full path.
"""

human_message = """\
File for which you have to generate overview:
\"\"\"
{submission_file}
\"\"\"\
"""
