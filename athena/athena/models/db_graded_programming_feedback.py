from typing import cast, Optional
from athena.schemas.programming_submission import ProgrammingSubmission
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from athena.database import Base, get_db
from .db_programming_submission import DBProgrammingSubmission
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


    def get_referenced_code(self) -> str:
        """
        Fetches the code from the submission repository.
        Might be quite an expensive operation!
        If there is no file_path, raises ValueError. If there are no given lines, returns the whole file.
        """
        if self.file_path is None:
            raise ValueError("file_path is None")
        with get_db() as db:
            db_submission = db.query(DBProgrammingSubmission).filter_by(id=self.submission_id).one()
            code = cast(ProgrammingSubmission, db_submission.to_schema()).get_code(self.file_path)
            if self.line_start is None:
                # return whole file
                return code
            if self.line_end is None:
                raise ValueError("Unexpected: line_start is not None, but line_end is None (only line_start given)")
            # Only return the lines between line_start and line_end. Line numbers are 0-based.
            return "\n".join(code.split("\n")[self.line_start : self.line_end + 1])
