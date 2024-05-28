from apted import APTED, Config
from typing import Dict, Iterable, List
import gc

from athena.helpers.programming.feedback import format_feedback_title
from athena.logger import logger
from athena.programming import Feedback, Submission

from module_programming_themisml.extract_methods import MethodNode, extract_methods
from module_programming_themisml.feedback_suggestions.batch import batched

# TODO This is a placeholder for computing the similarity score and give the right feedback. This is why themisCode is pasted in here.

APTED_THRESHOLD = 10  # TODO Needs to be adapted


def make_feedback_suggestion_from(feedback: Feedback, submission: Submission,
                                  submission_method: MethodNode) -> Feedback:
    suggestion = feedback.copy(deep=True)
    # add meta information for debugging
    suggestion.meta["original_feedback_id"] = feedback.id
    suggestion.meta["original_method_code"] = suggestion.meta["method_code"]
    suggestion.meta["method_code"] = submission_method.source_code
    # adjust for submission
    suggestion.submission_id = submission.id
    suggestion.line_start = submission_method.line_start
    suggestion.line_end = submission_method.line_end
    # regenerate title from filename and line numbers
    suggestion.title = format_feedback_title(suggestion.file_path, suggestion.line_start, suggestion.line_end)
    # remove ID
    suggestion.id = None
    return suggestion


# TODO: Stays the same


class CodeComparisonWithCorrespondingSuggestions:
    """A pair of code snippets with a corresponding suggestions if their similarity is high enough."""

    def __init__(self, code1: str, code2: str, tree1: str, tree2: str, suggestion: Feedback) -> None:
        self.code1 = code1
        self.code2 = code2
        self.tree1 = tree1
        self.tree2 = tree2
        self.suggestion = suggestion
        # TODO: Maybe create here also the tree for the code?

    def has_same_code(self, other) -> bool:
        return self.code1 == other.code1 and self.code2 == other.code2


def group_feedbacks_by_file_path(feedbacks: List[Feedback]) -> Dict[str, List[Feedback]]:
    """Groups feedbacks by file path for faster access."""
    feedbacks_by_file_path: Dict[str, List[Feedback]] = {}
    for feedback in feedbacks:
        if feedback.file_path not in feedbacks_by_file_path:
            feedbacks_by_file_path[str(feedback.file_path)] = []
        feedbacks_by_file_path[str(feedback.file_path)].append(feedback)
    return feedbacks_by_file_path


# TODO stays the same


def create_comparisons_with_suggestions(
        submissions: List[Submission],
        feedbacks: List[Feedback],
) -> Iterable[CodeComparisonWithCorrespondingSuggestions]:
    """Creates code comparisons and corresponding feedback suggestions as a generator."""
    if len(feedbacks) == 0:
        return
    # group feedbacks by file path for faster access
    logger.debug("Grouping %d feedbacks by file path", len(feedbacks))
    feedbacks_by_file_path = group_feedbacks_by_file_path(feedbacks)
    for submission in submissions:
        for file_path, file_feedbacks in feedbacks_by_file_path.items():
            # read file from submission
            try:
                code = submission.get_code(file_path)
            except KeyError:  # KeyError is for when the file is not in the zip
                logger.debug("File %s not found in submission %d.", file_path, submission.id)
                continue
            except UnicodeDecodeError:
                logger.warning("File %s in submission %d is not UTF-8 encoded.", file_path, submission.id)
                continue
            # get all methods in the file of the submission
            submission_methods = extract_methods(code)
            # TODO Hier die AST für die Methoden von der Submission generieren.
            # Erinnerung: nur die feedbacks haben bisher die ASTs

            # get all feedbacks that match methods in the submission
            for s_method in submission_methods:
                for feedback in file_feedbacks:
                    if feedback.submission_id == submission.id:
                        # don't compare feedback with itself
                        continue
                    if feedback.meta["method_name"] == s_method.name:
                        # compare code (later) and add feedback as a possible suggestion (also later)
                        suggestion = make_feedback_suggestion_from(feedback, submission, s_method)
                        # TODO Stays the same I only add also the ASTs hier von feedback and suggestion here to the method;
                        # suggestion doestn need to be changed
                        yield CodeComparisonWithCorrespondingSuggestions(s_method.source_code,
                                                                         feedback.meta["method_code"], suggestion)


def create_feedback_suggestions(
        submissions: List[Submission],
        feedbacks: List[Feedback],
) -> List[Feedback]:
    """
    Get a list of all submissions that the given feedback could also apply to (similar code in same method).
    Then generate feedback suggestions for those submissions.
    """
    if len(feedbacks) == 0:
        return []  # nothing to do

    suggestions: List[Feedback] = []

    # create code comparisons and corresponding feedback suggestions in batches for less memory usage
    for idx, comparisons_with_suggestions in enumerate(
            batched(create_comparisons_with_suggestions(submissions, feedbacks), 128)):
        # compute similarity scores for all comparisons at once
        sim_computer = CodeSimilarityComputer()
        # TODO Anstatt dem Computer meinen eigenen SimilarityCOmputer? - AP-TED usen brauche ich bestimmte Datenstrukturen?
        for s_comp in comparisons_with_suggestions:
            # TODO hier nicht den Code sondern den AST eingeben (oder beides Nullcheck?)
            sim_computer.add_comparison(s_comp.code1, s_comp.code2)
        logger.debug("Computing similarity scores for %d code comparisons (batch #%d)",
                     len(comparisons_with_suggestions), idx)
        sim_computer.compute_similarity_scores()  # compute all at once, enables vectorization

        # create suggestions
        for s_comp in comparisons_with_suggestions:
            similarity = sim_computer.get_similarity_score(s_comp.code1, s_comp.code2)
            if similarity.f1 >= APTED_THRESHOLD:
                # TODO Here meinen eigenen Threshold einfügen und die eigene Config überprüfen
                # found similar code -> create feedback suggestion
                logger.info("Found similar code with similarity score %s", similarity.f1)
                # add meta information for debugging
                s_comp.suggestion.meta["precision_score"] = similarity.precision
                s_comp.suggestion.meta["recall_score"] = similarity.recall
                s_comp.suggestion.meta["similarity_score"] = similarity.f1
                s_comp.suggestion.meta["similarity_score_f3"] = similarity.f3
                # add to suggestions
                suggestions.append(s_comp.suggestion)
        # clear memory to prevent being killed by OOM killer
        del sim_computer
        del comparisons_with_suggestions
        gc.collect()

    return suggestions