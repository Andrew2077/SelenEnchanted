"""
This module provides a set of decorators for error handling and logging in Selenium-based automation scripts.

Decorators:
    - check_nologger: Catches NoSuchElementException and other exceptions, returning None without logging.
    - check: Catches NoSuchElementException and other exceptions, logging the errors if logging is enabled.
    - retry: Retries a function a specified number of times (default is 3) if a StaleElementReferenceException occurs.
    - pass_if_crash: Continues execution if an error occurs, optionally logging the error message.

Classes:
    - ErrorHandler: Contains static methods for the above decorators.

Dependencies:
    - traceback: For formatting exception tracebacks.
    - typing: For type annotations.
    - selenium.common.exceptions: For handling Selenium-specific exceptions.
    - .logger: Custom Logger class for logging messages.

Usage:
    from decorators import ErrorHandler

    class MyClass:
        logger = Logger()
        log = True

        @ErrorHandler.check_nologger
        def my_method(self):
            # Method implementation

        @ErrorHandler.check
        def my_method_with_logging(self):
            # Method implementation

        @ErrorHandler.retry
        def my_method_with_retry(self):
            # Method implementation

        @ErrorHandler.pass_if_crash("Optional log message")
        def my_method_with_pass_if_crash(self):
            # Method implementation
"""

import traceback
from typing import Any, Callable, TypeVar, cast

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

from .logger import Logger

F = TypeVar("F", bound=Callable[..., Any])


class ErrorHandler:
    def check_nologger(func: F) -> F:
        """
        Decorator to catch NoSuchElementException and other exceptions, returning None without logging.

        Args:
            func (F): The function to be decorated.

        Returns:
            F: The wrapped function.
        """

        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except NoSuchElementException:
                return None
            except Exception:
                return None

        return wrapper

    def check(func: F) -> F:
        """
        Decorator to catch NoSuchElementException and other exceptions, logging the errors if logging is enabled.

        Args:
            func (F): The function to be decorated.

        Returns:
            F: The wrapped function.
        """

        def wrapper(self, *args, **kwargs):
            logger = cast(Logger, getattr(self, "logger", None))
            log = cast(bool, getattr(self, "log", False))
            try:
                return func(self, *args, **kwargs)

            except NoSuchElementException:
                tb = traceback.format_exc()
                if log:
                    logger.info(f"Element not found: {func.__name__} : {tb}")
                return None

            except Exception:
                tb = traceback.format_exc()
                if log:
                    logger.error(f"Error in {func.__name__}: {tb}")
                return None

        return wrapper

    def retry(func: F) -> F:
        """
        Decorator to retry a function a specified number of times (default is 3) if a StaleElementReferenceException occurs.

        Args:
            func (F): The function to be decorated.

        Returns:
            F: The wrapped function.
        """

        def wrapper(self, *args, **kwargs):
            logger = cast(Logger, getattr(self, "logger", None))
            for _ in range(3):
                try:
                    return func(self, *args, **kwargs)

                except StaleElementReferenceException:
                    continue

                except Exception:
                    tb = traceback.format_exc()
                    logger.error(f"Error in {func.__name__}: {tb}")
                    continue
            else:
                return None

        return wrapper

    def pass_if_crash(log_msg: str = "") -> Callable[[F], F]:
        """
        Decorator to continue execution if an error occurs, optionally logging the error message.

        Args:
            log_msg (str, optional): The log message to be used. Defaults to "".

        Returns:
            Callable[[F], F]: The decorator function.
        """

        def decorator(func: F) -> F:
            def wrapper(self, *args, **kwargs):
                logger = cast(Logger, getattr(self, "logger", None))
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    if logger == "":
                        pass
                    elif logger:
                        logger.error(f"{log_msg} - Error in {func.__name__}: {e}")
                    else:
                        print(
                            f"{log_msg} - Error in {func.__name__}: {e}"
                        )  # Fallback if logger is None

            return cast(F, wrapper)

        return decorator
