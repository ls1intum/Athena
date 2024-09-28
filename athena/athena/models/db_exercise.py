from sqlalchemy import Column, String, Float, UniqueConstraint, JSON, Enum as SqlEnum

from athena.schemas import ExerciseType
from .model import Model
from .big_integer_with_autoincrement import BigIntegerWithAutoincrement


class DBExercise(Model):
    __table_args__ = (UniqueConstraint('lms_url'),)

    id = Column(BigIntegerWithAutoincrement, primary_key=True, index=True, nullable=False)
    lms_url = Column(String, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    type = Column(SqlEnum(ExerciseType), index=True, nullable=False)
    max_points = Column(Float, index=True, nullable=False)
    bonus_points = Column(Float, index=True, nullable=False)
    grading_instructions = Column(String)
    problem_statement = Column(String)
    grading_criteria = Column(JSON, nullable=True)
    meta = Column(JSON, nullable=False)
