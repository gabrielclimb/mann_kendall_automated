"""
Logging configuration for the Mann-Kendall package.

This module provides centralized logging configuration for the entire package.
"""

import logging
import sys
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None,
) -> logging.Logger:
    """
    Configure logging for the Mann-Kendall package.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file. If None, logs to console only.
        format_string: Optional custom format string. Uses default if None.

    Returns:
        Configured logger instance

    Examples:
        >>> logger = setup_logging(level="DEBUG")
        >>> logger.info("Processing started")
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Get the root logger for this package
    logger = logging.getLogger("mann_kendall")
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_formatter = logging.Formatter(format_string)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_formatter = logging.Formatter(format_string)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Name of the module (typically __name__)

    Returns:
        Logger instance

    Examples:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing well data")
    """
    return logging.getLogger(f"mann_kendall.{name}")


# Default logger instance
default_logger = setup_logging()
