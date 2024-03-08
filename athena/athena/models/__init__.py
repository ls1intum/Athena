"""Models are SQLAlchemy classes that represent database tables."""
# Read
# https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/database/sqlalchemy.html#importing-all-sqlalchemy-models
# about possible issues with circular imports here.

from .db_exercise import DBExercise
from .db_submission import DBSubmission
from .db_graded_feedback import DBGradedFeedback
from .db_programming_exercise import DBProgrammingExercise
from .db_text_exercise import DBTextExercise
from .db_modelling_exercise import DBModellingExercise
from .db_programming_submission import DBProgrammingSubmission
from .db_text_submission import DBTextSubmission
from .db_modelling_submission import DBModellingSubmission
from .db_graded_programming_feedback import DBGradedProgrammingGradedFeedback
from .db_graded_text_feedback import DBGradedTextGradedFeedback
from .db_graded_modelling_feedback import DBGradedModellingGradedFeedback