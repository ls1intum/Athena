from typing import cast
from sqlalchemy import ForeignKey, Column, String
from sqlalchemy.orm import relationship

from athena.database import Base, get_db
from .db_submission import DBSubmission
from .big_integer_with_autoincrement import BigIntegerWithAutoincrement
from athena.schemas.programming_submission import ProgrammingSubmission


class DBProgrammingSubmission(DBSubmission, Base):
    __tablename__ = "programming_submissions"
    repository_url: str = Column(String, nullable=False)  # type: ignore

    exercise_id = Column(BigIntegerWithAutoincrement, ForeignKey("programming_exercises.id", ondelete="CASCADE"),
                         index=True)

    exercise = relationship("DBProgrammingExercise", back_populates="submissions")
    graded_feedbacks = relationship("DBGradedProgrammingFeedback", back_populates="submission")
    non_graded_feedbacks = relationship("DBNonGradedProgrammingFeedback", back_populates="submission")

    def get_referenced_code(self, file_path, line_start, line_end) -> str:
        """
        Fetches the code from the submission repository.
        Might be quite an expensive operation!
        If there is no file_path, raises ValueError. If there are no given lines, returns the whole file.
        """
        if file_path is None:
            raise ValueError("file_path is None")
        with get_db() as db:
            db_submission = db.query(DBProgrammingSubmission).filter_by(id=self.id).one()
            code = cast(ProgrammingSubmission, db_submission.to_schema()).get_code(file_path)
            if line_start is None:
                # return whole file
                return code
            if line_end is None:
                raise ValueError("Unexpected: line_start is not None, but line_end is None (only line_start given)")
            # Only return the lines between line_start and line_end. Line numbers are 0-based.
            return "\n".join(code.split("\n")[line_start: line_end + 1])
