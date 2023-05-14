from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from athena.database import Base

class DBTextBlock(Base):
    __tablename__ = "text_blocks"

    id = Column(String, primary_key=True, index=True)
    text = Column(String)
    start_index = Column(Integer)
    end_index = Column(Integer)
    added_distance = Column(Float, nullable=True, default=None)

    # foreign keys
    submission_id = Column(Integer, ForeignKey("text_submissions.id"))  # FK to athena-native table
    cluster_id = Column(Integer, ForeignKey("text_clusters.id"))  # FK to custom table

    submission = relationship("DBTextSubmission")
    cluster = relationship("DBTextCluster")

    def distance_to(self, other):
        """
        Returns the distance between this block and another block.
        """
        return self.cluster.distance_between_blocks(self, other)

    def __str__(self):
        return f"TextBlock{{id={self.id}, submission_id={self.submission_id} text='{self.text}', start='{self.start}', end='{self.end}', added_distance='{self.added_distance}', cluster_id='{self.cluster_id}'}}"
