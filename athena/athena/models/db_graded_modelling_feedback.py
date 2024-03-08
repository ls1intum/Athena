from typing import Optional

from sqlalchemy import Column, ForeignKey, JSON
from sqlalchemy.orm import relationship

from athena.database import Base
from .db_graded_feedback import DBGradedFeedback
from .big_integer_with_autoincrement import BigIntegerWithAutoincrement


class DBGradedModellingGradedFeedback(DBGradedFeedback, Base):
    __tablename__ = "graded_modelling_feedbacks"

    element_ids: Optional[list[str]] = Column(JSON)  # type: ignore

    exercise_id = Column(BigIntegerWithAutoincrement, ForeignKey("modelling_exercises.id", ondelete="CASCADE"), index=True)
    submission_id = Column(BigIntegerWithAutoincrement, ForeignKey("modelling_submissions.id", ondelete="CASCADE"), index=True)

    exercise = relationship("DBModellingExercise", back_populates="feedbacks")
    submission = relationship("DBModellingSubmission", back_populates="feedbacks")
