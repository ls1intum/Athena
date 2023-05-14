import struct
from typing import List, Iterable

from athena.database import get_db
from athena.logger import logger
from module_cofee.models.db_text_cluster import DBTextCluster
from module_cofee.protobuf import cofee_pb2
from module_cofee.models.db_text_block import DBTextBlock


def store_text_blocks(segments: List[cofee_pb2.Segment]):
    """Convert segments to text blocks and store them in the DB."""
    for segment in segments:
        # store text block in DB
        with get_db() as db:
            model = DBTextBlock(
                id=segment.id,
                submission_id=segment.submissionId,
                text=segment.text,
                start_index=segment.startIndex,
                end_index=segment.endIndex,
            )
            db.merge(model)
            db.commit()


def float_list_to_bytes(floats: List[float]) -> bytes:
    """Convert a list of floats to a bytes object."""
    return struct.pack('{}f'.format(len(floats)), *floats)


def store_text_clusters(exercise_id: int, clusters: Iterable[cofee_pb2.Cluster]):
    """"""
    for cluster in clusters:
        distance_matrix = [entry.value for entry in cluster.distanceMatrix]
        # store text cluster in DB
        with get_db() as db:
            model = DBTextCluster(
                exercise_id=exercise_id,
                distance_matrix=float_list_to_bytes(distance_matrix),
            )
            print(model)
            db.merge(model)
            db.commit()


def process_results(clusters: List[cofee_pb2.Cluster], segments: List[cofee_pb2.Segment], exercise_id):
    """Processes results coming back from the CoFee system via callbackUrl"""
    logger.debug(f"Received {len(clusters)} clusters and {len(segments)} segments from CoFee")
    store_text_blocks(segments)
    store_text_clusters(exercise_id, clusters)
    logger.debug("Finished processing CoFee results")
