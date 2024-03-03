from sqlalchemy import Column, BigInteger, Boolean, Float

from athena.models.feedback.db_feedback import DBFeedback


class DBGradedFeedback(DBFeedback):
    credits = Column(Float, nullable=False)
    structured_grading_instruction_id = Column(BigInteger)

    # not in the schema, but used in the database to distinguish between feedbacks and feedback suggestions
    is_suggestion = Column(Boolean, default=False, nullable=False)
