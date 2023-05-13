from typing import List

from athena.logger import logger
from module_cofee.protobuf import cofee_pb2


def parse_text_blocks(segments: List[cofee_pb2.Segment], exercise_id: int):
    """"""
    ...


def parse_text_clusters(clusters: List[cofee_pb2.Cluster]):
    """"""
    ...


def process_clusters(text_clusters, text_block_map, exercise_id: int):
    """"""
    ...


def process_results(clusters: List[cofee_pb2.Cluster], segments: List[cofee_pb2.Segment], exercise_id):
    """Processes results coming back from the CoFee system via callbackUrl"""
    logger.debug(f"Received {len(clusters)} clusters and {len(segments)} segments from CoFee")
    text_blocks = parse_text_blocks(segments, exercise_id)
    text_clusters = parse_text_clusters(clusters)
    process_clusters(text_clusters, text_blocks, exercise_id)
    logger.debug("Finished processing CoFee results")
