"""
logger.py

This module provides a singleton Logger class for logging messages to both console and files.
It uses the SingletonMeta metaclass to ensure that only one instance of the Logger class exists.

Classes:
    Logger: A singleton class for logging messages.

Usage:
    from logger import Logger

    logger = Logger(log_dir='logs', console_logging=True, clear_logs=False, logs_name='app_logs')
    logger.info('This is an info message')
    logger.error('This is an error message')
"""

import logging
import os
from ..utilities.meta_classes import SingletonMeta


class Logger(metaclass=SingletonMeta):
    """
    A singleton class for logging messages to both console and files.

    Attributes:
        log_dir (str): The directory where log files will be stored.
        console_logging (bool): Flag to enable or disable console logging.
        clear_logs (bool): Flag to clear existing logs on initialization.
        logs_name (str): The name of the log files.

    Methods:
        __call__(message: str): Logs an info message.
        debug(message: str): Logs a debug message.
        info(message: str): Logs an info message.
        warning(message: str): Logs a warning message.
        error(message: str): Logs an error message.
        critical(message: str): Logs a critical message.
        clear_log_file(): Clears the content of the log files.
    """

    def __init__(
        self,
        log_dir: str,
        console_logging: bool = True,
        clear_logs: bool = False,
        logs_name: str = None,
    ):
        """
        Initializes the Logger instance.

        Args:
            log_dir (str): The directory where log files will be stored.
            console_logging (bool): Flag to enable or disable console logging.
            clear_logs (bool): Flag to clear existing logs on initialization.
            logs_name (str): The name of the log files.
        """
        self.log_dir = os.path.join(log_dir, logs_name)
        os.makedirs(self.log_dir, exist_ok=True)

        self.all_log_path = os.path.join(self.log_dir, "all.log")
        self.warn_error_log_path = os.path.join(self.log_dir, "warn_error.log")

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        if console_logging:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        file_handler = logging.FileHandler(
            self.all_log_path, mode="a", encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        warn_error_file_handler = logging.FileHandler(
            self.warn_error_log_path, mode="a", encoding="utf-8"
        )
        warn_error_file_handler.setLevel(logging.WARNING)
        warn_error_file_handler.setFormatter(formatter)
        self.logger.addHandler(warn_error_file_handler)

        if clear_logs:
            self.clear_log_file()

    def __call__(self, message: str):
        """
        Logs an info message.

        Args:
            message (str): The message to log.
        """
        return self.info(message)

    def debug(self, message: str):
        """
        Logs a debug message.

        Args:
            message (str): The message to log.
        """
        self.logger.debug(message)

    def info(self, message: str):
        """
        Logs an info message.

        Args:
            message (str): The message to log.
        """
        self.logger.info(message)

    def warning(self, message: str):
        """
        Logs a warning message.

        Args:
            message (str): The message to log.
        """
        self.logger.warning(message)

    def error(self, message: str):
        """
        Logs an error message.

        Args:
            message (str): The message to log.
        """
        self.logger.error(message)

    def critical(self, message: str):
        """
        Logs a critical message.

        Args:
            message (str): The message to log.
        """
        self.logger.critical(message)

    def clear_log_file(self) -> None:
        """
        Clears the content of the log files.
        """
        try:
            with open(self.all_log_path, "w") as log_dir:
                log_dir.truncate(0)

            with open(self.warn_error_log_path, "w") as log_dir:
                log_dir.truncate(0)

        except FileNotFoundError:
            print(f"Log file not found at {self.log_dir}")
