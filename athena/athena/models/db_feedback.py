from sqlalchemy import Column, BigInteger, Boolean, String, Float, JSON, UniqueConstraint

from .model import Model
from .big_integer_with_autoincrement import BigIntegerWithAutoincrement


class DBFeedback(Model):
    __table_args__ = (UniqueConstraint('lms_id'),)

    id = Column(BigIntegerWithAutoincrement, primary_key=True, index=True, autoincrement=True)
    lms_id = Column(BigInteger)
    title = Column(String)
    description = Column(String)
    meta = Column(JSON, nullable=False)
