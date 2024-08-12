"""
profiler.py

This module provides a Profiler class that can be used to profile the execution time of methods and functions,
as well as trace errors that occur during their execution. The Profiler class uses a SingletonMeta metaclass to
ensure that only one instance of the Profiler exists.

Classes:
    Profiler: A singleton class that provides decorators for profiling and error tracing.

Functions:
    Profiler.timeit_method(func: Callable) -> Callable:
        Logs the time taken for a method to run.
        
    Profiler.timeit_function(self, func: Callable) -> Callable:
        Logs the time taken for a function to run.
        
    Profiler.trace_error_method(func: Callable) -> Callable:
        Logs the error if a method fails.

Usage:
    To use the Profiler, decorate your methods or functions with the provided decorators.
    Example:
        @Profiler.timeit_method
        def some_method(self):
            # method implementation

        @Profiler.timeit_function
        def some_function():
            # function implementation

        @Profiler.trace_error_method
        def another_method(self):
            # method implementation
"""

from __future__ import annotations

import os
import time
import traceback
from typing import Any, Callable, TypeVar, cast

from ..components.tab import Tab
from ..utilities import exceptions as Exceptions
from ..utilities.meta_classes import SingletonMeta
from ..utilities.logger import Logger

F = TypeVar("F", bound=Callable[..., Any])


class Profiler(metaclass=SingletonMeta):
    """
    A singleton class that provides decorators for profiling and error tracing.

    Attributes:
        _apply_profiling (bool): A flag to enable or disable profiling.
    """

    _apply_profiling = True

    @staticmethod
    def timeit_method(func: Callable) -> Callable:
        """
        Logs the time taken for a method to run.

        Args:
            func (Callable): The method to be profiled.

        Returns:
            Callable: The wrapped method with profiling.
        """

        def wrapper(self, *args, **kwargs):
            if Profiler._apply_profiling:
                logger = cast(Logger, getattr(self, "logger", None))
                start = time.monotonic()
                result = func(self, *args, **kwargs)
                end = time.monotonic()
                logger.info(
                    f"Time taken : {end - start:.4f} at {func.__name__} form {func.__module__}"
                )

                return result
            else:
                return func(self, *args, **kwargs)

        return wrapper

    def timeit_function(self, func: Callable) -> Callable:
        """
        Logs the time taken for a function to run.

        Args:
            func (Callable): The function to be profiled.

        Returns:
            Callable: The wrapped function with profiling.
        """

        def wrapper(*args, **kwargs):
            if Profiler._apply_profiling:
                start = time.monotonic()
                result = func(*args, **kwargs)
                end = time.monotonic()
                print(
                    f"Time taken : {end - start:.4f} at {func.__name__} form {func.__module__}"
                )
                return result
            else:
                return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def trace_error_method(func: Callable) -> Callable:
        """
        Logs the error if a method fails.

        Args:
            func (Callable): The method to be traced for errors.

        Returns:
            Callable: The wrapped method with error tracing.
        """

        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                return result
            except Exception as e:
                logger = cast(Logger, getattr(self, "logger", None))
                tab = cast(Tab, getattr(self, "core", None))
                error_trace = traceback.format_exc()
                logger.error(
                    f"Error at {func.__name__} form {func.__module__} : \n{error_trace}"
                )

                screen_dir = f"{logger.log_dir}/profiler_screens"
                os.makedirs(screen_dir, exist_ok=True)
                screen_path = f"{screen_dir}/{func.__name__}.png"
                tab.screen(screen_path)
                raise Exceptions.ExecutionFailedException(
                    f"Error at {func.__name__} form {func.__module__} : \n{error_trace}"
                )

        return wrapper
