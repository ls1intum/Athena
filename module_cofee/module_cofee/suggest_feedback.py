from typing import List

from athena.database import get_db
from athena.text import Submission, Feedback
from module_cofee.models.db_text_block import DBTextBlock


DISTANCE_THRESHOLD = 1.0

def suggest_feedback_from_cluster(submission: Submission) -> List[Feedback]:
    """
    Suggest feedback for a submission based on existing feedback & processed clusters.
    """
    with get_db() as db:
        # get blocks of submission
        blocks = db.query(DBTextBlock).filter_by(submission_id=submission.id).all()
        # get all feedbacks ever given on the exercise
        exercise_submissions = db.query(Submission).filter_by(exercise_id=submission.exercise_id).all()
        exercise_feedbacks = (f for s in exercise_submissions for f in s.feedbacks)
    suggestions: List[Feedback] = []
    for block in blocks:
        # if TextBlock is part of a cluster and the cluster is not disabled, we try to find an existing Feedback Element
        if block.cluster and not block.cluster.disabled:
            all_blocks_in_cluster = block.cluster.blocks
            ids_of_blocks_in_cluster = (b.id for b in all_blocks_in_cluster)
            cluster_feedbacks = [  # all feedback given on text blocks in the cluster
                f for f in exercise_feedbacks
                if f.reference in ids_of_blocks_in_cluster
            ]
            if cluster_feedbacks:
                # find the closest block that has feedback
                all_blocks_in_cluster_with_feedback = (
                    b for b in all_blocks_in_cluster
                    if any(f.reference == b.id for f in cluster_feedbacks)
                )
                try:
                    closest_block = min(
                        all_blocks_in_cluster_with_feedback,
                        key=lambda b: b.distance_to(block)
                    )
                except ValueError:
                    # no block in cluster has feedback
                    continue
                if closest_block.distance_to(block) >= DISTANCE_THRESHOLD:
                    # if the closest block is too far away, we don't suggest feedback
                    continue
                # find the feedback that was given on the closest block
                similar_feedbacks = (
                    f for f in cluster_feedbacks
                    if f.reference == closest_block.id
                )
                # add original feedback ID to metadata for debugging purposes
                for f in similar_feedbacks:
                    f.meta['original_feedback_id'] = f.id
                    f.meta['original_submission_id'] = f.submission_id
                # add feedbacks to suggestions, but for the new submission
                new_feedbacks = (
                    f.copy(submission_id=submission.id)
                    for f in similar_feedbacks
                )
                suggestions.extend(new_feedbacks)
    return suggestions
