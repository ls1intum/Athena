from typing import List, cast

from athena.database import get_db
from athena.models import DBTextFeedback
from athena.text import GradedFeedback


def get_exercise_feedbacks(exercise_id: int) -> List[GradedFeedback]:
    """
    Get all feedback on a given exercise.
    """
    with get_db() as db:
        return [
            cast(GradedFeedback, f.to_schema())
            for f in db.query(DBTextFeedback).filter_by(exercise_id=exercise_id).all()
        ]