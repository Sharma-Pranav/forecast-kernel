
import logging
import os
import sys

def setup_logger(log_path: str = None, logger_name: str = "forecast"):
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