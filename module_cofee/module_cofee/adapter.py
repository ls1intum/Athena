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

try:
    from module_cofee.protobuf import cofee_pb2
except ImportError as e:
    if "cofee_pb2" in str(e):
        raise ImportError("Could not import protobuf module. Please run `make protobuf` to generate it.")
    else:
        raise e


def get_cofee_url() -> str:
    """
    Get the URL of the CoFee service from the environment variable COFEE_URL.
    """
    return os.environ["COFEE_URL"]


def send_submissions(exercise: Exercise, submissions: List[Submission]):
    """Send submissions to old Athena-CoFee server."""
    logger.info(f"Sending {len(submissions)} submissions to CoFee")
    resp = requests.post(
        f"{get_cofee_url()}/submit",
        json={
            "courseId": exercise.course_id,
            # TODO: maybe make this more flexible?
            "callbackUrl": f"http://localhost:{os.environ['PORT']}/cofee_callback",
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
            "Authorization": os.environ["COFEE_AUTH_TOKEN"],
        },
    )
    resp.raise_for_status()
    logger.info("Submissions sent to CoFee")


@app.post("/cofee_callback/{exercise_id}")
async def save_athene_result(exercise_id: int, request: Request):
    """
    Saves automatic textAssessments of Athena.
    """
    logger.info("Received callback from CoFee")
    cofee_resp = cofee_pb2.AtheneResponse.FromString(await request.body())
    clusters = cofee_resp.clusters
    segments = cofee_resp.segments