from typing import Optional
from enum import Enum

from pydantic import Field

from .submission import Submission


class TextSubmission(Submission):
    """Submission on a text exercise."""
    model: str = Field()
