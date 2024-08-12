"""
tab.py

This module provides the `Tab` class which represents a browser tab and allows
various operations to be performed on it using Selenium WebDriver.

Classes:
--------
Tab
    A class to represent a browser tab and perform various operations on it.

"""

import base64
import os
from io import BytesIO

import requests
from PIL import Image
from selenium.webdriver.remote.webdriver import WebDriver

from ..utilities.decorators import ErrorHandler
from ..utilities.logger import Logger
from ..utilities.sleeper import Sleeper


class Tab:
    """
    A class to represent a browser tab and perform various operations on it.

    Attributes:
    ----------
    driver : WebDriver
        The WebDriver instance to interact with the browser.
    logger : Logger
        The Logger instance to log information.
    sleeper : Sleeper
        The Sleeper instance to handle sleep operations.
    """

    def __init__(
        self,
        driver: WebDriver,
        logger: Logger,
    ):
        """
        Constructs all the necessary attributes for the Tab object.

        Parameters:
        ----------
        driver : WebDriver
            The WebDriver instance to interact with the browser.
        logger : Logger
            The Logger instance to log information.
        """
        self.driver = driver
        self.logger = logger
        self.sleeper = Sleeper()

    @ErrorHandler.retry
    def get_url(self, url: str, remove_translation: bool = True):
        """
        Navigates to the given URL with optional translation removal.

        Parameters:
        ----------
        url : str
            The URL to navigate to.
        remove_translation : bool, optional
            Flag to remove translation parameters from the URL (default is True).

        Returns:
        -------
        bool
            True if navigation is successful.
        """
        if remove_translation:
            url = url.split("locale")[0]
        self.driver.get(url)
        self.logger.info(f"Navigated to {url}")
        return True

    def get(self, url: str):
        """
        Navigates to the given URL without removing translation parameters.

        Parameters:
        ----------
        url : str
            The URL to navigate to.
        """
        self.get_url(url, remove_translation=False)

    def open_new_window(self, url):
        """
        Opens a new window and navigates to the given URL.

        Parameters:
        ----------
        url : str
            The URL to navigate to in the new window.
        """
        self.driver.execute_script(self.js.OPEN_NEW_WINDOW)
        last_handled_window = len(self.driver.window_handles)
        self.driver.switch_to.window(
            self.driver.window_handles[last_handled_window - 1]
        )
        self.driver.get(url)

    def switch_window(self, window_number: int):
        """
        Switches to the window with the given index.

        Parameters:
        ----------
        window_number : int
            The index of the window to switch to.
        """
        self.driver.switch_to.window(self.driver.window_handles[window_number])

    def close_last_opened_window(self):
        """
        Closes the last opened window and switches to the previous one.
        """
        self.driver.close()
        last_handled_window = len(self.driver.window_handles)
        self.driver.switch_to.window(
            self.driver.window_handles[last_handled_window - 1]
        )

    def back_url(self):
        """
        Navigates back to the previous URL in the browser history.
        """
        self.driver.back()

    def close(self, timeout: int = 2):
        """
        Closes the browser tab after a specified timeout.

        Parameters:
        ----------
        timeout : int, optional
            The time to wait before closing the tab (default is 2 seconds).
        """
        self.sleeper.wait(timeout)
        self.driver.close()
        self.logger.info("Driver closed")

    def screen(self, name: str = "test"):
        """
        Takes a screenshot of the current browser window.

        Parameters:
        ----------
        name : str, optional
            The name of the screenshot file (default is "test").
        """
        if ".png" not in name:
            name += ".png"
        self.driver.save_screenshot(name)

    def save_image(self, url: str, path: str):
        """
        Saves an image from the given URL to the specified path.
        Args:
            url (str): The URL of the image to be saved.
            path (str): The path where the image will be saved.
        Raises:
            requests.exceptions.RequestException: If there is an error while saving the image.
        Returns:
            None
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(path, "wb") as out_file:
                out_file.write(response.content)
            self.logger.info(f"Image saved at {path}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error saving image from {url} to {path}: {str(e)}")

    def save_base64_image(self, base64_image_data: str, path: str) -> None:
        """
        Converts a Base64-encoded image data to a PIL image and saves it to a file.

        Args:
            base64_image_data (str): The Base64-encoded image data.
            path (str): The path where the image will be saved.
        """
        base64_image_data = base64_image_data.split(",")[1]
        image_data = base64.b64decode(base64_image_data)
        image = Image.open(BytesIO(image_data))
        image.save(path)
        self.logger.info(f"Image saved at {path}")

    def download_content(self, src: str, path: str, name: str):
        """
        Downloads a video from the given source URL and saves it to the specified path with the given name.

        Args:
            src (str): The URL of the video source.
            path (str): The path where the video will be saved.
            name (str): The name of the video file.

        Returns:
            None

        Raises:
            None
        """
        try:
            response = requests.get(src)
            if response.status_code == 200:
                with open(os.path.join(path, name), "wb") as video_file:
                    video_file.write(response.content)
                    video_file.close()
                    self.logger.info(f"successfully downloaded {name}")
            else:
                self.logger.info(
                    "Failed to download the video. Status code:", response.status_code
                )
        except Exception as e:
            self.logger.info("Failed to download the video. Error:", e)
