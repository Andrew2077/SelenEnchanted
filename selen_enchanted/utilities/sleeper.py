"""
Sleeper Module

This module provides the Sleeper class, which introduces delays in the execution of a program. 
The delays can be either fixed or random within specified duration categories.

Classes:
    Sleeper: A singleton class that provides methods for introducing delays.

Usage:
    from sleeper import Sleeper

    sleeper = Sleeper()
    sleeper.catigorized_random_wait("medium")
    sleeper.catigorized_fixed_wait("short")
"""

import random
import time
from typing import Optional, Tuple
from ..utilities.meta_classes import SingletonMeta


class Sleeper(metaclass=SingletonMeta):
    """
    A singleton class that provides methods for introducing delays in the execution of a program.

    Attributes:
        TIME_VERY_LOW (Tuple[float, float]): Duration range for very low time.
        TIME_LOW (Tuple[float, float]): Duration range for low time.
        TIME_MEDIUM (Tuple[float, float]): Duration range for medium time.
        TIME_HIGH (Tuple[float, float]): Duration range for high time.
        TIME_VERY_HIGH (Tuple[float, float]): Duration range for very high time.
        FIXED_TIMEOUT_ASYSNC_BLINK (float): Fixed timeout for async blink.
        FIXED_TIMEOUT_ASYNC_VERY_LOW (int): Fixed timeout for async very low time.
        FIXED_TIMEOUT_ASYNC_LOW (int): Fixed timeout for async low time.
        FIXED_TIMEOUT_ASYNC_MEDIUM (int): Fixed timeout for async medium time.
        FIXED_TIMEOUT_ASYNC_HIGH (int): Fixed timeout for async high time.
        FIXED_TIMEOUT_ASYNC_VERY_HIGH (int): Fixed timeout for async very high time.
    """

    def __init__(self) -> None:
        self.TIME_VERY_LOW = (0.5, 1)
        self.TIME_LOW = (1, 2)
        self.TIME_MEDIUM = (2, 3)
        self.TIME_HIGH = (3, 4)
        self.TIME_VERY_HIGH = (4, 5)

        self.FIXED_TIMEOUT_ASYSNC_BLINK = 0.5
        self.FIXED_TIMEOUT_ASYNC_VERY_LOW = 1
        self.FIXED_TIMEOUT_ASYNC_LOW = 2
        self.FIXED_TIMEOUT_ASYNC_MEDIUM = 3
        self.FIXED_TIMEOUT_ASYNC_HIGH = 4
        self.FIXED_TIMEOUT_ASYNC_VERY_HIGH = 5

    def catigorized_random_wait(
        self, duration: str, custom_duration: Optional[Tuple[int, int]] = None
    ) -> None:
        """
        Waits for a random time within a specified duration category or a custom duration.

        The predefined categories and their corresponding durations are as follows:
        - "very_short": 0.5 to 1 second
        - "short": 1 to 2 seconds
        - "medium": 2 to 3 seconds
        - "long": 3 to 4 seconds
        - "very_long": 4 to 5 seconds

        If the duration category is not recognized, the function defaults to "very low".
        Args:
            duration (str): The category of the duration. It can be one of the following: "very low", "low", "medium", "high", "very high". If the category is not recognized, the function defaults to "medium".
            custom_duration (Optional[Tuple[int, int]]): A tuple of two integers representing the minimum and maximum delay in seconds. If provided, this duration is used instead of the predefined categories.
        """
        duration_mapping = {
            "very_short": self.TIME_VERY_LOW,
            "short": self.TIME_LOW,
            "medium": self.TIME_MEDIUM,
            "long": self.TIME_HIGH,
            "very_long": self.TIME_VERY_HIGH,
        }

        if duration not in duration_mapping:
            print(f"Invalid duration '{duration}', using default duration 'very_short'")
            duration = "very_short"

        wait_time = custom_duration if custom_duration else duration_mapping[duration]
        self.wait_random_time(*wait_time)

    def catigorized_fixed_wait(self, duration: str):
        """
        Waits for a random time within a specified duration category or a custom duration.
        This function is used to introduce a random delay in the execution of the program. The delay is either within a predefined category or a custom duration provided by the user.
        The predefined categories and their corresponding durations are as follows:
        - "very_short": 1 second
        - "short": 2 seconds
        - "medium": 3 seconds
        - "long": 4 seconds
        - "very_long": 5 seconds

        If the duration category is not recognized, the function defaults to "medium".

        Args:
        - duration (str): The category of the duration. It can be one of the following: "very low", "low", "medium", "high", "very high". If the category is not recognized, the function defaults to "medium".
        - custom_duration (Optional[Tuple[int, int]]): A tuple of two integers representing the minimum and maximum delay in seconds. If provided, this duration is used instead of the predefined categories.
        """
        duration_mapping = {
            "very_short": self.FIXED_TIMEOUT_ASYNC_VERY_LOW,
            "short": self.FIXED_TIMEOUT_ASYNC_LOW,
            "medium": self.FIXED_TIMEOUT_ASYNC_MEDIUM,
            "long": self.FIXED_TIMEOUT_ASYNC_HIGH,
            "very_long": self.FIXED_TIMEOUT_ASYNC_VERY_HIGH,
        }

        if duration not in duration_mapping:
            print(f"Invalid duration '{duration}', using default duration 'medium'")
            duration = "medium"

        self.wait(duration_mapping[duration])

    def wait(self, duration: int):
        """
        Waits for a fixed amount of time.

        Args:
            duration (int): The amount of time to wait in seconds.
        """
        time.sleep(duration)

    def wait_random_time(self, min_duration: int, max_duration: int):
        """
        Waits for a random amount of time between the specified minimum and maximum durations.

        Args:
            min_duration (int): The minimum amount of time to wait in seconds.
            max_duration (int): The maximum amount of time to wait in seconds.
        """
        duration = random.uniform(min_duration, max_duration)
        time.sleep(duration)
