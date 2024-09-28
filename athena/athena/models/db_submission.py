from sqlalchemy import Column, JSON, String, UniqueConstraint

from .model import Model
from .big_integer_with_autoincrement import BigIntegerWithAutoincrement


class DBSubmission(Model):
    __table_args__ = (UniqueConstraint('lms_url'),)

    id = Column(BigIntegerWithAutoincrement, primary_key=True, index=True, autoincrement=True,)
    lms_url = Column(String, index=True, nullable=False)
    meta = Column(JSON, nullable=False)
