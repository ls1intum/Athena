"""Common place for environment variables with sensible defaults for local development."""
import os

PRODUCTION = os.environ.get("PRODUCTION", "0") == "1"
