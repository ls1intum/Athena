from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from athena.database import Base
from .db_exercise import DBExercise


class DBProgrammingExercise(DBExercise, Base):
    __tablename__ = "programming_exercises"

    programming_language: str = Column(String, nullable=False)  # type: ignore
    solution_repository_url: str = Column(String, nullable=False) # type: ignore
    template_repository_url: str = Column(String, nullable=False) # type: ignore
    tests_repository_url: str = Column(String, nullable=False)  # type: ignore

    submissions = relationship("DBProgrammingSubmission", back_populates="exercise")
    graded_feedbacks = relationship("DBGradedProgrammingFeedback", back_populates="exercise")
    non_graded_feedbacks = relationship("DBNonGradedProgrammingFeedback", back_populates="exercise")
