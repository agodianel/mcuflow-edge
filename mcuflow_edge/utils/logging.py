"""Logging configuration for MCUflow-Edge."""

import logging

__all__ = ["logger", "setup_logging"]


def setup_logging(level: int = logging.INFO) -> None:
    """Configure logging for the mcue CLI.

    Call this once at CLI startup rather than at module import time
    to avoid side effects when importing the library.
    """
    logging.basicConfig(
        level=level,
        format="%(levelname)s %(name)s: %(message)s",
    )


logger = logging.getLogger("mcue")
