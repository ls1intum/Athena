from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from athena.database import Base
from .db_feedback import DBFeedback


class DBProgrammingFeedback(DBFeedback, Base):
    __tablename__ = "programming_feedbacks"

    file_path: str = Column(String)  # type: ignore
    line_start: int = Column(Integer)  # type: ignore
    line_end: int = Column(Integer)  # type: ignore

    exercise_id = Column(Integer, ForeignKey("programming_exercises.id", ondelete="CASCADE"), index=True)
    submission_id = Column(Integer, ForeignKey("programming_submissions.id", ondelete="CASCADE"), index=True)

    exercise = relationship("DBProgrammingExercise", back_populates="feedbacks")
    submission = relationship("DBProgrammingSubmission", back_populates="feedbacks")
