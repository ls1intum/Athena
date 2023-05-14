from typing import List, Iterable

from athena.database import get_db
from athena.models import DBTextSubmission
from athena.text import Submission, Feedback
from module_cofee.models.db_text_block import DBTextBlock


DISTANCE_THRESHOLD = 1.0


def get_exercise_feedbacks(exercise_id: int) -> List[Feedback]:
    """
    Get all feedback on a given exercise.
    """
    with get_db() as db:
        return db.query(Feedback).filter_by(exercise_id=exercise_id).all()


def filter_feedbacks_by_block(feedbacks: List[Feedback], block: DBTextBlock) -> Iterable[Feedback]:
    """
    Filter a list of feedback to only contain feedback that is linked to a given block.
    """
    return (
        f for f in feedbacks
        if block.feedback_is_linked_to_block(f)
    )


def suggest_feedback_for_block(submission: Submission, block: DBTextBlock) -> List[Feedback]:
    """
    Suggest feedback for a text block (part of submission) based on existing feedback & processed clusters.
    """
    # Find the cluster that this block belongs to
    cluster = block.cluster
    # If the cluster is disabled, there should be no suggestions
    if cluster.disabled:
        return []
    # Get all blocks of that cluster
    blocks = cluster.blocks
    # Only consider blocks for which there is feedback available at all
    exercise_feedbacks = get_exercise_feedbacks(submission.exercise_id)
    blocks_with_feedback = (
        block
        for block in blocks
        if any(filter_feedbacks_by_block(exercise_feedbacks, block))
    )
    # Find the closest block to this block
    closest_block = min(
        blocks_with_feedback,
        key=lambda other_block: block.distance_to(other_block),
    )
    # If the distance is too large, there should be no suggestions
    if block.distance_to(closest_block) >= DISTANCE_THRESHOLD:
        return []
    # Get all feedbacks on the closest block
    suggested_feedback = filter_feedbacks_by_block(exercise_feedbacks, closest_block)
    # add new submission ID, link the feedback to the block and add meta information for debugging
    suggested_feedback = [
        f.copy(
            submission_id=submission.id,
            meta={
                **f.meta,
                "block_id": block.id,
                "original_submission_id": submission.id,
                "original_block_id": closest_block.id,
            },
        )
        for f in suggested_feedback
    ]
    return suggested_feedback


def suggest_feedback_for_submission(submission: Submission) -> List[Feedback]:
    """
    Suggest feedback for a submission based on existing feedback & processed clusters.
    """
    with get_db() as db:
        # get blocks of submission
        blocks = db.query(DBTextBlock).filter_by(submission_id=submission.id).all()
        # merge suggestions for all blocks
        return [
            suggestion
            for block in blocks
            for suggestion in suggest_feedback_for_block(submission, block)
        ]
