from typing import Optional

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from athena.database import Base
from .db_feedback import DBFeedback
from .big_integer_with_autoincrement import BigIntegerWithAutoincrement


class DBModellingFeedback(DBFeedback, Base):
    __tablename__ = "modelling_feedbacks"

    exercise_id = Column(BigIntegerWithAutoincrement, ForeignKey("modelling_exercises.id", ondelete="CASCADE"), index=True)
    submission_id = Column(BigIntegerWithAutoincrement, ForeignKey("modelling_submissions.id", ondelete="CASCADE"), index=True)

    exercise = relationship("DBModellingExercise", back_populates="feedbacks")
    submission = relationship("DBModellingSubmission", back_populates="feedbacks")
