from typing import List, Iterable

from athena.logger import logger
from module_cofee.models.text_cluster import TextCluster
from module_cofee.protobuf import cofee_pb2
from module_cofee.models.text_block import TextBlock


def store_text_blocks(segments: List[cofee_pb2.Segment]):
    """Convert segments to text blocks and store them in the DB."""
    for segment in segments:
        # store text block in DB
        TextBlock(
            id=segment.id,
            submission_id=segment.submissionId,
            text=segment.text,
            start_index=segment.startIndex,
            end_index=segment.endIndex,
        ).save()


def store_text_clusters(exercise_id: int, clusters: Iterable[cofee_pb2.Cluster]):
    """"""
    for cluster in clusters:
        distance_matrix = [[entry.value for entry in row] for row in cluster.distanceMatrix]
        # store text cluster in DB
        TextCluster(
            id=cluster.id,
            exercise_id=exercise_id,
            distance_matrix=distance_matrix,
        ).save()


def process_results(clusters: List[cofee_pb2.Cluster], segments: List[cofee_pb2.Segment], exercise_id):
    """Processes results coming back from the CoFee system via callbackUrl"""
    logger.debug(f"Received {len(clusters)} clusters and {len(segments)} segments from CoFee")
    store_text_blocks(segments)
    store_text_clusters(exercise_id, clusters)
    logger.debug("Finished processing CoFee results")
