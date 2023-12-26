"""
Entry point for the assessment module manager.
"""
import uvicorn

from assessment_module_manager import endpoints, env
from assessment_module_manager.app import app
from assessment_module_manager.logger import logger


def main():
    """
    Start the assessment module manager using uvicorn.
    """
    logger.info("Starting assessment module manager")

    if env.PRODUCTION:
        logger.info("Running in PRODUCTION mode")
        uvicorn.run("assessment_module_manager.__main__:app", host="0.0.0.0", port=5100)
    else:
        logger.warning("Running in DEVELOPMENT mode")
        uvicorn.run("assessment_module_manager.__main__:app", host="0.0.0.0", port=5100, reload=True)


# Add things to __all__ just to mark them as important to import
__all__ = ["app", "endpoints", "main"]
if __name__ == "__main__":
    main()
