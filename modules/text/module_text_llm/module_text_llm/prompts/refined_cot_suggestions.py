system_message = """
         You gave the following feedback on the first iteration: {answer}
         On this step you need to refine your feedback.
         Make sure to follow the following steps to assess and improve your feedback:
         It shuold follow the grading instructions and the sample solution, if it doesn't, consider improvements.
         If you have your own additional improvements that are not present in the grading instructions, add them in a new feedback with 0 credits and no reference.
         Remember that your response is directly seen by students and it should adress them directly.
         For each feedback where the student has room for improvement, think about how the student could improve his solution.
         Once you have thought how the student can improve the solution, formulate it in a way that guides the student towards the correct solution without revealing it directly.
         Consider improvements to the feedback if any of this points is not satisfied."""

human_message = """\
Student\'s submission to grade (with sentence numbers <number>: <sentence>):
\"\"\"
{submission}
\"\"\"\
"""