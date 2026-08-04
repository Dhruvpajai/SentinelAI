"""
Logging configuration for SentinelAI.

Writes structured logs to both console and rotating log files.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from backend.core.config import Settings


def setup_logging(settings: Settings) -> None:
    """
    Configure application-wide logging.

    Args:
        settings: Application settings containing log level and directory.
    """
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "sentinelai.log"
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Avoid duplicate handlers on reload
    if root_logger.handlers:
        root_logger.handlers.clear()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    logging.getLogger("uvicorn.access").setLevel(log_level)
