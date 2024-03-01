from typing import Iterable, Union, Type, Optional, List

from athena.database import get_db
from athena.schemas import GradedFeedback


def get_stored_feedback(
        feedback_cls: Type[GradedFeedback], exercise_id: int, submission_id: Union[int, None]
) -> Iterable[GradedFeedback]:
    """
    Returns a list of feedbacks for the given exercise in the given submission.
    If submission_id is None, returns all feedbacks for the given exercise.
    """
    db_feedback_cls = feedback_cls.get_model_class()
    with get_db() as db:
        query = db.query(db_feedback_cls).filter_by(exercise_id=exercise_id, is_suggestion=0)
        if submission_id is not None:
            query = query.filter_by(submission_id=submission_id)
        return (f.to_schema() for f in query.all())


def get_stored_feedback_meta(feedback: GradedFeedback) -> Optional[dict]:
    """Returns the stored metadata associated with the feedback."""
    db_feedback_cls = feedback.__class__.get_model_class()
    with get_db() as db:
        return db.query(db_feedback_cls.meta).filter_by(id=feedback.id).scalar()  # type: ignore


def store_feedback(feedback: GradedFeedback, is_lms_id=False) -> GradedFeedback:
    """Stores the given LMS feedback.

    Args:
        feedback (GradedFeedback): The feedback to store.
        is_lms_id (bool, optional): Whether the feedback's ID is an LMS ID. Defaults to False.
    
    Returns:
        GradedFeedback: The stored feedback with its internal ID assigned.
    """
    db_feedback_cls = feedback.__class__.get_model_class()
    with get_db() as db:
        lms_id = None
        if is_lms_id:
            lms_id = feedback.id
            internal_id = db.query(db_feedback_cls.id).filter_by(lms_id=lms_id).scalar()  # type: ignore
            feedback.id = internal_id

        stored_feedback_model = db.merge(feedback.to_model(lms_id=lms_id))
        db.commit()
        return stored_feedback_model.to_schema()


def get_stored_feedback_suggestions(
        feedback_cls: Type[GradedFeedback], exercise_id: int, submission_id: int
) -> Iterable[GradedFeedback]:
    """Returns a list of feedback suggestions for the given exercise in the given submission."""
    db_feedback_cls = feedback_cls.get_model_class()
    with get_db() as db:
        query = db.query(db_feedback_cls).filter_by(exercise_id=exercise_id, is_suggestion=True)
        if submission_id is not None:
            query = query.filter_by(submission_id=submission_id)
        return (f.to_schema() for f in query.all())


def store_graded_feedback_suggestions(feedbacks: List[GradedFeedback]) -> List[GradedFeedback]:
    """Stores the given feedbacks as a suggestions.

    Returns:
        List[GradedFeedback]: The stored feedback suggestions with their internal IDs assigned.
    """
    stored_feedbacks: List[GradedFeedback] = []
    with get_db() as db:
        for feedback in feedbacks:
            stored_feedback_model = db.merge(feedback.to_model(is_suggestion=True))
            db.flush() # Ensure the ID is generated now
            stored_feedbacks.append(stored_feedback_model.to_schema())
        db.commit()
    return stored_feedbacks


def store_feedback_suggestion(feedback: GradedFeedback):
    """Stores the given feedback as a suggestion."""
    store_graded_feedback_suggestions([feedback])
