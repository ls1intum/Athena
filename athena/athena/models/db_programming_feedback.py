from typing import cast
from athena.schemas.programming_submission import ProgrammingSubmission
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from athena.database import Base, get_db
from .db_programming_submission import DBProgrammingSubmission
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


    def get_code(self):
        """
        Fetches the code from the submission repository.
        Might be quite an expensive operation!
        """
        if self.file_path is None:
            raise ValueError("file_path is None")
        if self.line_start is None:
            raise ValueError("line_start is None")
        with get_db() as db:
            submission = db.query(DBProgrammingSubmission).filter_by(id=self.submission_id).one()
            code = cast(ProgrammingSubmission, submission.to_schema()).get_code(self.file_path)
            line_end = self.line_end if self.line_end is not None else self.line_start
            return "\n".join(code.split("\n")[self.line_start:line_end + 1])
