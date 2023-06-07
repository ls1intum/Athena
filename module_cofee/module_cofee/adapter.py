"""
Adapter functions to connect to the actual CoFee service, which still has an older API.
"""
import os
from typing import List

from fastapi import Request
import requests

from athena import app
from athena.text import Exercise, Submission
from athena.logger import logger
from athena.module_config import get_module_config
from module_cofee.process_results import process_results

try:
    from module_cofee.protobuf import cofee_pb2
except ImportError as e:
    if "cofee_pb2" in str(e):
        raise ImportError("Could not import protobuf module. Please run `make protobuf` to generate it.") from e
    raise e


# Default token for local testing, from https://github.com/ls1intum/Athena/blob/master/.env
DEFAULT_COFEE_TOKEN = "YWVuaXF1YWRpNWNlaXJpNmFlbTZkb283dXphaVF1b29oM3J1MWNoYWlyNHRoZWUzb2huZ2FpM211bGVlM0VpcAo="


def get_cofee_url() -> str:
    """
    Get the URL of the CoFee service from the environment variable COFEE_URL.
    """
    return os.environ.get("COFEE_URL", "http://localhost")


def send_submissions(exercise: Exercise, submissions: List[Submission]):
    """Send submissions to old Athena-CoFee server."""
    logger.info("Sending %d submissions to CoFee", len(submissions))
    module_url = os.environ.get("MODULE_URL", f"http://localhost:{get_module_config().port}")
    resp = requests.post(
        f"{get_cofee_url()}/submit",
        json={
            # TODO: maybe make this more flexible?
            "callbackUrl": f"{module_url}/cofee_callback/{exercise.id}",
            "submissions": [
                {
                    "id": submission.id,
                    "text": submission.content,
                }
                for submission in submissions
            ],
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": os.environ.get("COFEE_AUTH_TOKEN", DEFAULT_COFEE_TOKEN),
        },
        timeout=60,
        # TODO: remove this again:
        verify=False,  # Ignore SSL errors for now, because athenetest1-01 has an invalid certificate
    )
    resp.raise_for_status()
    logger.info("Submissions sent to CoFee")


@app.post("/cofee_callback/{exercise_id}")
async def save_athene_result(exercise_id: int, request: Request):
    """
    Saves automatic textAssessments of Athena.
    """
    logger.info("Received callback from CoFee")
    cofee_resp = cofee_pb2.AtheneResponse.FromString(await request.body()) # type: ignore
    clusters = cofee_resp.clusters
    segments = cofee_resp.segments
    process_results(clusters, segments, exercise_id)
