"""Centralised logging configuration helpers."""

import logging
import os
import sys

def setup_logger(log_path: str = None, logger_name: str = "forecast"):
    """Initialise a basic logger that also writes to ``log_path`` if given.

    Parameters
    ----------
    log_path : str, optional
        File path for a rotating log file. If ``None`` only stdout is used.
    logger_name : str, optional
        Name for the created logger.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """

    handlers = [logging.StreamHandler(sys.stdout)]

    if log_path:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        handlers.append(logging.FileHandler(log_path, encoding="utf-8"))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=handlers
    )
    return logging.getLogger(logger_name)
