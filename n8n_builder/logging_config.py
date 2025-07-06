"""
Centralized logging configuration for N8N Builder.
Controls log levels and output based on environment variables.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, Optional

# Environment variable names
ENV_LOG_LEVEL = "N8N_LOG_LEVEL"
ENV_LOG_FILE_SIZE = "N8N_LOG_FILE_SIZE"
ENV_LOG_BACKUP_COUNT = "N8N_LOG_BACKUP_COUNT"
ENV_LOG_DIR = "N8N_LOG_DIR"

# Default values
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10MB
DEFAULT_LOG_BACKUP_COUNT = 5
DEFAULT_LOG_DIR = "logs"

# Log level mapping
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

def get_log_level() -> int:
    """Get log level from environment variable or default."""
    level = os.getenv(ENV_LOG_LEVEL, DEFAULT_LOG_LEVEL).upper()
    return LOG_LEVELS.get(level, logging.INFO)

def get_log_file_size() -> int:
    """Get maximum log file size from environment variable or default."""
    try:
        return int(os.getenv(ENV_LOG_FILE_SIZE, DEFAULT_LOG_FILE_SIZE))
    except ValueError:
        return DEFAULT_LOG_FILE_SIZE

def get_log_backup_count() -> int:
    """Get number of backup log files from environment variable or default."""
    try:
        return int(os.getenv(ENV_LOG_BACKUP_COUNT, DEFAULT_LOG_BACKUP_COUNT))
    except ValueError:
        return DEFAULT_LOG_BACKUP_COUNT

def get_log_dir() -> Path:
    """Get log directory from environment variable or default."""
    log_dir = os.getenv(ENV_LOG_DIR, DEFAULT_LOG_DIR)
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path

def setup_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with the specified name and optional log file.
    
    Args:
        name: Logger name (e.g., 'n8n_builder.validation')
        log_file: Optional specific log file name (without .log extension)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Don't add handlers if they already exist
    if logger.handlers:
        return logger
    
    # Set log level from environment
    logger.setLevel(get_log_level())
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # Console handler (always present)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file specified)
    if log_file:
        log_path = get_log_dir() / f"{log_file}.log"
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=get_log_file_size(),
            backupCount=get_log_backup_count()
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    This is the main entry point for getting loggers throughout the application.
    
    Args:
        name: Logger name (e.g., 'n8n_builder.validation')
    
    Returns:
        Configured logger instance
    """
    return setup_logger(name)

def setup_error_log_handler():
    """Attach a handler to the root logger for errors.log."""
    error_log_path = get_log_dir() / "errors.log"
    error_handler = RotatingFileHandler(
        error_log_path,
        maxBytes=get_log_file_size(),
        backupCount=get_log_backup_count()
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logging.getLogger().addHandler(error_handler)

# Create default loggers
validation_logger = get_logger('n8n_builder.validation')
retry_logger = get_logger('n8n_builder.retry')
diff_logger = get_logger('n8n_builder.diff')
error_logger = get_logger('n8n_builder.error')

# Attach global error handler
setup_error_log_handler() 