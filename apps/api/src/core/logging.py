"""
Structured Logging Configuration
Production-ready logging with JSON format
"""

import logging
import sys
from typing import Any, Dict
import structlog


def setup_logging() -> None:
    """Configure structured logging for the application"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


logger = structlog.get_logger()


def log_error(message: str, **kwargs: Any) -> None:
    """Log an error with additional context"""
    logger.error(message, **kwargs)


def log_warning(message: str, **kwargs: Any) -> None:
    """Log a warning with additional context"""
    logger.warning(message, **kwargs)


def log_info(message: str, **kwargs: Any) -> None:
    """Log an info message with additional context"""
    logger.info(message, **kwargs)


def log_debug(message: str, **kwargs: Any) -> None:
    """Log a debug message with additional context"""
    logger.debug(message, **kwargs)
