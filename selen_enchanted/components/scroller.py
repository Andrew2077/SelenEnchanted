"""
Scroller Module

This module provides the Scroller class to handle scrolling actions on a web page using Selenium WebDriver.

Classes:
    Scroller: A class to handle scrolling actions on a web page using Selenium WebDriver.
"""

import random
from time import monotonic
from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from ..core.javascripts import JavaScripts
from ..utilities import exceptions as Exceptions
from ..utilities.sleeper import Sleeper


class Scroller:
    """
    A class to handle scrolling actions on a web page using Selenium WebDriver.

    Attributes:
        driver (WebDriver): The Selenium WebDriver instance.
        js (JavaScripts): An instance of JavaScripts to execute JavaScript commands.
        sleeper (Sleeper): An instance of Sleeper to handle wait times.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Initializes the Scroller with a WebDriver instance.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        self.driver = driver
        self.js = JavaScripts
        self.sleeper = Sleeper()

    def scroll_element(self, element: WebElement):
        """
        Scrolls to the bottom of an element using JavaScript.

        Args:
            element (WebElement): The element to scroll to the bottom of.
        """
        self.driver.execute_script(self.js.SCROLL_TO_ELEMENT, element)

    def scroll_to_element(self, element: WebElement):
        """
        Scrolls to a WebElement.

        Args:
            element (WebElement): The element to scroll into view.

        Raises:
            Exceptions.ScrollFailedException: If scrolling fails.
        """
        try:
            self.driver.execute_script(self.js.SCROLL_INTO_VIEW, element)
        except Exception as exc:
            raise Exceptions.ScrollFailedException() from exc
        self.sleeper.catigorized_random_wait("very_short")

    def scroll_page(self, length: int = 5000):
        """
        Scrolls the page by a specified length using Selenium.

        Args:
            length (int, optional): The length to scroll. Defaults to 5000.

        Raises:
            Exceptions.ScrollFailedException: If scrolling fails.
        """
        try:
            self.driver.execute_script(self.js.SCROLL_WITH_LENGTH, length)
        except Exception as exc:
            raise Exceptions.ScrollFailedException() from exc

    def scroll_like_mouse(
        self,
        scroll_length: Tuple[int, int] = (35, 120),
        scrolls_count: int = None,
        timeout: float = 0.03,
    ) -> None:
        """
        Scrolls the page in a manner similar to a mouse scroll, with variable lengths and pauses.

        Args:
            scroll_length (Tuple[int, int], optional): The range of scroll lengths. Defaults to (35, 120).
            scrolls_count (int, optional): The number of scrolls. If None, a random number between 50 and 100 is used. Defaults to None.
            timeout (float, optional): The pause time between scrolls. Defaults to 0.03.
        """
        if scrolls_count is None or isinstance(scrolls_count, int) is False:
            scrolls_count = random.randint(50, 100)
        for _ in range(scrolls_count):
            random_length = random.randint(*scroll_length)
            self.scroll_page(random_length)
            self.sleeper.wait(timeout)

    def scroll_like_mouse_to_element(
        self,
        element: WebElement,
        scroll_length: Tuple[int, int] = (35, 120),
        timeout: float = 0.03,
        tolerance: float = 0.7,
    ) -> None:
        """
        Scrolls towards an element like a mouse with variable scroll lengths and pauses.

        Args:
            element (WebElement): The element to scroll towards.
            scroll_length (Tuple[int, int], optional): The range of scroll lengths. Defaults to (35, 120).
            timeout (float, optional): The pause time between scrolls. Defaults to 0.03.
            tolerance (float, optional): The tolerance for considering the element centered. Defaults to 0.7.
        """
        start_time = monotonic()
        while not self._is_element_centered_in_viewport(element):
            target_y = self.driver.execute_script(self.js.GET_ELEMENT_HIGHT, element)
            random_length = random.randint(*scroll_length)
            if target_y > 0:
                self.scroll_page(random_length)
            else:
                self.scroll_page(-random_length)
            self.sleeper.wait(timeout)
            if self._is_element_centered_in_viewport(element, tolerance):
                return

            if monotonic() - start_time > 15:
                self.scroll_to_element(element)
                return

    def _is_element_centered_in_viewport(
        self, element: WebElement, tolerance: float = 0.7
    ) -> bool:
        """
        Checks if the specified element is centered within the viewport, within a given tolerance.

        Args:
            element (WebElement): The element to check.
            tolerance (float, optional): The tolerance for considering the element centered. Defaults to 0.7.

        Returns:
            bool: True if the element is centered within the viewport, False otherwise.
        """
        return self.driver.execute_script(
            self.js.IS_ELEMENT_VISIBLE, element, tolerance
        )
