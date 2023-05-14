from sqlalchemy import Column, Integer, LargeBinary, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from athena.database import Base


class DBTextCluster(Base):
    __tablename__ = "text_clusters"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    probabilities = Column(LargeBinary)
    distance_matrix = Column(LargeBinary)
    disabled = Column(Boolean, default=False)

    # Define the relationship to TextBlock
    blocks = relationship("DBTextBlock", back_populates="cluster")

    # Define the relationship to TextExercise
    exercise_id = Column(Integer, ForeignKey('text_exercises.id'))
    exercise = relationship("DBTextExercise")

    def __str__(self):
        return f"TextCluster{{id={self.id}, exercise_id={self.exercise_id}, probabilities={self.probabilities}, distance_matrix={self.distance_matrix}, disabled={self.disabled}}}"
