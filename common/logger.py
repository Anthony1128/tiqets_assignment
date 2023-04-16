import logging
import os
import sys


class AppLogger:
    """Application logger with custom configuration."""

    def __init__(self):
        self.output_file_path = "output.log"

    def init_logger(self):
        """Method to get logger instance."""
        logger = logging.getLogger("tiqets_app")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(format)
        log_filepath = os.path.join(os.path.abspath(os.curdir), self.output_file_path)
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(format)
        logger.addHandler(handler)
        logger.addHandler(file_handler)
        return logger


app_logger = AppLogger().init_logger()
