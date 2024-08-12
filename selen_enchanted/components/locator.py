"""
locator.py

This module contains the Locator class, which provides methods to find web elements using Selenium WebDriver and WebDriverWait.

Classes:
--------
Locator
    A class to locate web elements using various strategies.

"""

from typing import List, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from ..utilities.logger import Logger
from ..utilities import exceptions as Exceptions


class Locator:
    """
    Locator class to find web elements using Selenium WebDriver.

    Attributes:
        driver (WebDriver): The Selenium WebDriver instance.
        logger (Logger): The logger instance for logging errors and information.
    """

    def __init__(self, driver: WebDriver, logger: Logger):
        """
        Initializes the Locator with a WebDriver and a Logger.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            logger (Logger): The logger instance for logging errors and information.
        """
        self.driver = driver
        self.logger = logger

    def find_elements(
        self,
        method: By = By.XPATH,
        val: str = None,
        parent: Optional[WebElement] = None,
        timeout: int = 5,
    ) -> List[WebElement]:
        """
        Finds multiple web elements given a method, value, and timeout.

        Args:
            method (By): The method to locate elements (default is By.XPATH).
            val (str): The value to locate elements.
            parent (Optional[WebElement]): The parent web element to search within (default is None).
            timeout (int): The timeout in seconds to wait for elements (default is 5).

        Returns:
            List[WebElement]: A list of found web elements. Returns an empty list if no elements are found.
        """
        if parent:
            try:
                WebDriverWait(self.driver, timeout / 2).until(EC.staleness_of(parent))
                return []
            except TimeoutException:
                pass
        else:
            parent = self.driver

        try:
            selected_elements = WebDriverWait(parent, timeout).until(
                EC.presence_of_all_elements_located((method, val))
            )
        except TimeoutException:
            return []

        except StaleElementReferenceException:
            self.logger.error("StaleElementReferenceException")
            return []

        return selected_elements

    def find_element(
        self,
        method: By,
        val: str,
        parent: Optional[WebElement] = None,
        timeout: int = 5,
    ) -> WebElement:
        """
        Finds a single web element given a method, value, and timeout.

        Args:
            method (By): The method to locate the element.
            val (str): The value to locate the element.
            parent (Optional[WebElement]): The parent web element to search within (default is None).
            timeout (int): The timeout in seconds to wait for the element (default is 5).

        Returns:
            WebElement: The found web element.

        Raises:
            Exceptions.ExpectedElementNotFoundException: If the element is not found within the timeout or if it is no longer in the DOM.
        """
        if parent is None:
            parent = self.driver

        try:
            element = WebDriverWait(parent, timeout).until(
                EC.presence_of_element_located((method, val))
            )
            return element

        except TimeoutException:
            raise Exceptions.ExpectedElementNotFoundException(
                f"Element not found within timeout, identified selector: {method} : {val}"
            ) from None

        except StaleElementReferenceException:
            raise Exceptions.ExpectedElementNotFoundException(
                f"Element no longer found in the DOM, identified selector: {method} : {val}"
            ) from None
