from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from athena.database import Base
from .db_graded_feedback import DBGradedFeedback
from .big_integer_with_autoincrement import BigIntegerWithAutoincrement


class DBGradedProgrammingGradedFeedback(DBGradedFeedback, Base):
    __tablename__ = "graded_programming_feedbacks"

    file_path: Optional[str] = Column(String)  # type: ignore
    line_start: Optional[int] = Column(Integer)  # type: ignore
    line_end: Optional[int] = Column(Integer)  # type: ignore

    exercise_id = Column(BigIntegerWithAutoincrement, ForeignKey("programming_exercises.id", ondelete="CASCADE"), index=True)
    submission_id = Column(BigIntegerWithAutoincrement, ForeignKey("programming_submissions.id", ondelete="CASCADE"), index=True)

    exercise = relationship("DBProgrammingExercise", back_populates="feedbacks")
    submission = relationship("DBProgrammingSubmission", back_populates="feedbacks")