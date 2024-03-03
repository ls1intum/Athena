from typing import Optional

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from athena.database import Base
from athena.models.feedback.graded_feedback.db_graded_feedback import DBGradedFeedback
from athena.models.big_integer_with_autoincrement import BigIntegerWithAutoincrement


class DBGradedTextFeedback(DBGradedFeedback, Base):
    __tablename__ = "graded_text_feedbacks"

    index_start: Optional[int] = Column(Integer)  # type: ignore
    index_end: Optional[int] = Column(Integer)  # type: ignore

    exercise_id = Column(BigIntegerWithAutoincrement, ForeignKey("text_exercises.id", ondelete="CASCADE"), index=True)
    submission_id = Column(BigIntegerWithAutoincrement, ForeignKey("text_submissions.id", ondelete="CASCADE"), index=True)

    exercise = relationship("DBTextExercise", back_populates="feedbacks")
    submission = relationship("DBTextSubmission", back_populates="feedbacks")
