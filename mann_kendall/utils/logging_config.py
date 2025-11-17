"""
Logging configuration for the Mann-Kendall package.

This module provides centralized logging configuration for the entire package.
Logging is lazily initialized to avoid creating handlers at import time.
"""

import logging
import sys
from typing import Optional

# Track if logging has been configured
_logging_configured = False


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None,
) -> logging.Logger:
    """
    Configure logging for the Mann-Kendall package.

    This function should be called explicitly by applications using the package
    to set up logging with desired settings. If not called, loggers will use
    Python's default configuration (WARNING level, no handlers).

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file. If None, logs to console only.
        format_string: Optional custom format string. Uses default if None.

    Returns:
        Configured logger instance

    Examples:
        >>> logger = setup_logging(level="DEBUG")
        >>> logger.info("Processing started")

        >>> # Configure with file output
        >>> logger = setup_logging(level="INFO", log_file="analysis.log")
    """
    global _logging_configured

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

    _logging_configured = True
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    This returns a child logger under the 'mann_kendall' namespace.
    Logging configuration should be set up by calling setup_logging()
    before using loggers, otherwise Python's default logging configuration
    will be used (WARNING level, no handlers).

    Args:
        name: Name of the module (typically __name__)

    Returns:
        Logger instance

    Examples:
        >>> # In application code, configure logging first
        >>> setup_logging(level="INFO")
        >>>
        >>> # Then get loggers in modules
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing well data")
    """
    return logging.getLogger(f"mann_kendall.{name}")


def is_logging_configured() -> bool:
    """
    Check if logging has been explicitly configured.

    Returns:
        True if setup_logging() has been called, False otherwise

    Examples:
        >>> if not is_logging_configured():
        ...     setup_logging()
    """
    return _logging_configured


def reset_logging() -> None:
    """
    Reset logging configuration.

    Removes all handlers from the mann_kendall logger and resets
    the configuration state. Useful for testing or reconfiguration.

    Examples:
        >>> reset_logging()
        >>> setup_logging(level="DEBUG")  # Reconfigure with new settings
    """
    global _logging_configured
    logger = logging.getLogger("mann_kendall")
    logger.handlers.clear()
    logger.setLevel(logging.NOTSET)
    _logging_configured = False

