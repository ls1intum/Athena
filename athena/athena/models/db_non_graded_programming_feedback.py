from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from athena.database import Base
from .db_non_graded_feedback import DBNonGradedFeedback
from .big_integer_with_autoincrement import BigIntegerWithAutoincrement


class DBNonGradedProgrammingFeedback(DBNonGradedFeedback, Base):
    __tablename__ = "non_graded_programming_feedbacks"

    file_path: Optional[str] = Column(String)  # type: ignore
    line_start: Optional[int] = Column(Integer)  # type: ignore
    line_end: Optional[int] = Column(Integer)  # type: ignore

    exercise_id = Column(BigIntegerWithAutoincrement, ForeignKey("programming_exercises.id", ondelete="CASCADE"), index=True)
    submission_id = Column(BigIntegerWithAutoincrement, ForeignKey("programming_submissions.id", ondelete="CASCADE"), index=True)

    exercise = relationship("DBProgrammingExercise", back_populates="non_graded_feedbacks")
    submission = relationship("DBProgrammingSubmission", back_populates="non_graded_feedbacks")
