"""
This module provides the Actions class which encapsulates various user interaction methods
using Selenium WebDriver. These actions include clicking, pressing keys, hovering, and 
manipulating web elements in a browser.

Classes:
    Actions: Encapsulates user interaction methods using Selenium WebDriver.
"""

import os
from typing import Tuple, Union

from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from ..core.javascripts import JavaScripts
from ..utilities.logger import Logger
from ..utilities.sleeper import Sleeper
from .scroller import Scroller


class Actions:
    """
    Encapsulates various user interaction methods using Selenium WebDriver.
    """

    def __init__(self, driver: webdriver, logger: Logger):
        """
        Initializes the Actions class with a WebDriver instance and a Logger.

        Args:
            driver (webdriver.Chrome): The WebDriver instance to interact with the browser.
            logger (Logger): The Logger instance for logging actions.
        """
        self.driver = driver
        self.logger = logger
        self.keys = Keys()
        self.action_chain = ActionChains(self.driver)
        self.sleeper = Sleeper()
        self.scroller = Scroller(self.driver)
        self.js = JavaScripts

    def click_on(self, x_coord: int, y_coord: int, delay: int = 1):
        """
        Performs a click action at the given x and y coordinates.

        Args:
            x_coord (int): The x-coordinate to click.
            y_coord (int): The y-coordinate to click.
            delay (int, optional): The delay before performing the click. Defaults to 1.
        """
        action = ActionChains(self.driver)
        action.move_by_offset(x_coord, y_coord)
        action.pause(delay)
        action.click()
        action.perform()

    def press_esc(self):
        """
        Simulates pressing the Escape key.
        """
        self.action_chain.key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()
        self.sleeper.catigorized_random_wait("very_short")

    def press_key(self, key: str):
        """
        Simulates pressing a specified arrow key.

        Args:
            key (str): The arrow key to press ('right', 'left', 'up', 'down').
        """
        if key.lower() == "right":
            self.action_chain.key_down(self.keys.ARROW_RIGHT).key_up(
                self.keys.ARROW_RIGHT
            ).perform()
        elif key.lower() == "left":
            self.action_chain.key_down(self.keys.ARROW_LEFT).key_up(
                self.keys.ARROW_LEFT
            ).perform()
        elif key.lower() == "up":
            self.action_chain.key_down(self.keys.ARROW_UP).key_up(
                self.keys.ARROW_UP
            ).perform()
        elif key.lower() == "down":
            self.action_chain.key_down(self.keys.ARROW_DOWN).key_up(
                self.keys.ARROW_DOWN
            ).perform()

    def click_by_mouse(self, element: WebElement, num_clicks: int = 1):
        """
        Clicks on a web element using the mouse.

        Args:
            element (WebElement): The web element to click.
            num_clicks (int, optional): The number of clicks to perform. Defaults to 1.
        """
        self.scroller.scroll_to_element(element)
        for _ in range(num_clicks):
            try:
                self.action_chain.move_to_element(element).click().perform()
            except JavascriptException:
                element.click()
        self.sleeper.catigorized_random_wait("short")

    def calc_element_center(self, element: WebElement) -> Tuple[int, int]:
        """
        Calculates the center coordinates of a web element.

        Args:
            - element (WebElement): The web element to calculate the center of.

        Returns:
            - Tuple[int, int]: The x and y coordinates of the center of the element.
        """
        x_c = element.location["x"] + element.size["width"] // 2
        y_c = element.location["y"] + element.size["height"] // 2
        return x_c, y_c

    def click_on_location(self, x: int, y: int):
        """
        Clicks on a specific location using JavaScript.

        Args:
            x (int): The x-coordinate to click.
            y (int): The y-coordinate to click.
        """
        self.driver.execute_script(self.js.PERFORM_MOUSE_CLICK, x, y)
        self.sleeper.catigorized_random_wait("very_short")

    def highlight_element(self, element: WebElement):
        """
        Highlights a web element using JavaScript.

        Args:
            element (WebElement): The web element to highlight.
        """
        self.driver.execute_script(self.js.HIGHLIGHT_ELEMENT, element)

    def mark_current_position_with_dot(self):
        """
        Marks the current cursor position with a dot using JavaScript.
        """
        self.driver.execute_script(self.js.CREATE_BLUE_DOT)

    def get_current_cursor_coords(self) -> Tuple[int, int]:
        """
        Retrieves the current cursor coordinates.

        Returns:
            Tuple[int, int]: The x and y coordinates of the current cursor position.
        """
        cursor_position = self.driver.execute_async_script(self.js.GET_CURSOR_COORDS)
        return cursor_position

    def hover(
        self, element: WebElement, timeout: Union[str, int] = "very_short"
    ) -> None:
        """
        Hovers over a web element.

        Args:
            element (WebElement): The web element to hover over.
            timeout (Union[str, int], optional): The timeout duration. Defaults to "very_short".
        """
        self.scroller.scroll_to_element(element)
        self.action_chain.move_to_element(element).perform()
        if isinstance(timeout, str):
            self.sleeper.catigorized_random_wait(timeout)
        else:
            self.sleeper.wait(timeout)

    def hover_over_coordinates(self, x: int, y: int, click: bool = False):
        """
        Hovers over specific coordinates and optionally clicks.

        Args:
            x (int): The x-coordinate to hover over.
            y (int): The y-coordinate to hover over.
            click (bool, optional): Whether to click at the coordinates. Defaults to False.
        """
        if click:
            self.action_chain.move_by_offset(x, y).click().perform()
        self.action_chain.move_by_offset(x, y).perform()
        self.sleeper.catigorized_random_wait("very_short")

    def move_cursor_and_mark(self, x: int, y: int):
        """
        Moves the cursor to specific coordinates and marks the position with a dot.

        Args:
            x (int): The x-coordinate to move the cursor to.
            y (int): The y-coordinate to move the cursor to.
        """
        self.driver.execute_script(self.js.MOVE_CURSOR_AND_CREATE_DOT, x, y)

    def ensure_transition(self):
        """
        Ensures a transition by pressing Escape and waiting.
        """
        self.press_esc()
        self.sleeper.catigorized_random_wait("very_short")

    def clear_input(self, input_element: WebElement):
        """
        Clears the input field of a web element.

        Args:
            input_element (WebElement): The web element whose input field to clear.
        """
        if os.name == "nt":
            select_all = Keys.CONTROL + "a"
            input_element.send_keys(select_all)
            input_element.send_keys(Keys.DELETE)
        else:
            val = input_element.get_attribute("value")
            for i in range(len(val)):
                self.sleeper.wait(0.03)
                input_element.send_keys(Keys.BACKSPACE)

    def send_keys_letter_by_letter(self, element: WebElement, data: str):
        """
        Sends keys to a web element one by one.

        Args:
            element (WebElement): The web element to send keys to.
            data (str): The string data to send.
        """
        for char in data:
            element.send_keys(char)
            self.sleeper.wait_random_time(0.03, 0.06)
