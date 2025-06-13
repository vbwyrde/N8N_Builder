import os
import logging
from n8n_builder.logging_config import validation_logger, retry_logger, diff_logger, error_logger

def test_logging():
    print("Testing logging configuration...")
    print(f"N8N_LOG_LEVEL: {os.getenv('N8N_LOG_LEVEL', 'NOT SET')}")
    print(f"Log files should be in: {os.getenv('N8N_LOG_DIR', 'logs')}")

    # Validation logger
    validation_logger.debug("[DEBUG] Validation logger test.")
    validation_logger.info("[INFO] Validation logger test.")
    validation_logger.warning("[WARNING] Validation logger test.")
    validation_logger.error("[ERROR] Validation logger test.")
    validation_logger.critical("[CRITICAL] Validation logger test.")

    # Retry logger
    retry_logger.debug("[DEBUG] Retry logger test.")
    retry_logger.info("[INFO] Retry logger test.")
    retry_logger.warning("[WARNING] Retry logger test.")
    retry_logger.error("[ERROR] Retry logger test.")
    retry_logger.critical("[CRITICAL] Retry logger test.")

    # Diff logger
    diff_logger.debug("[DEBUG] Diff logger test.")
    diff_logger.info("[INFO] Diff logger test.")
    diff_logger.warning("[WARNING] Diff logger test.")
    diff_logger.error("[ERROR] Diff logger test.")
    diff_logger.critical("[CRITICAL] Diff logger test.")

    # Error logger
    error_logger.debug("[DEBUG] Error logger test.")
    error_logger.info("[INFO] Error logger test.")
    error_logger.warning("[WARNING] Error logger test.")
    error_logger.error("[ERROR] Error logger test.")
    error_logger.critical("[CRITICAL] Error logger test.")

    print("Logging test complete. Check your console and log files for output.")

if __name__ == "__main__":
    test_logging() 