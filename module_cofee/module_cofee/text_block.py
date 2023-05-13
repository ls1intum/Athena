import hashlib
from dataclasses import dataclass
from enum import Enum

class TextBlockType(Enum):
    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"

@dataclass
class TextBlock:
    id: str = ""
    text: str = ""
    start_index: int = 0
    end_index: int = 0
    number_of_affected_submissions: int = 0
    type: TextBlockType = TextBlockType.MANUAL
    position_in_cluster: int = None
    added_distance: float = None
    knowledge: 'TextAssessmentKnowledge' = None
    cluster: 'TextCluster' = None

    def __str__(self):
        return f"TextBlock{{id={self.id}, text='{self.text}', startIndex='{self.start_index}', endIndex='{self.end_index}', type='{self.type}'}}"
