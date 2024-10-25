"""
driver.py

This module provides the ChromeDriver class, which is used to initialize and manage a Chrome WebDriver instance with various options and configurations.
"""

import time
from typing import Optional

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.remote.webdriver import WebDriver
from seleniumwire import webdriver as wire_driver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

from ..utilities.logger import Logger
from .options import OptionsMode


class ChromeDriver:
    """
    ChromeDriver class to initialize and manage a Chrome WebDriver instance.

    Attributes:
        options (Options): Chrome options for the WebDriver.
        logger (Logger): Logger instance for logging information.
        driver (WebDriver): The Chrome WebDriver instance.
    """

    def __init__(
        self,
        options: Optional[Options] = None,
        use_driver_manger: bool = False,
        driver: Optional[WebDriver] = None,
        logger: Optional[Logger] = None,
        use_wire: bool = False,
        wire_options: Optional[dict] = None,
    ) -> None:
        """
        Initializes the ChromeDriver instance with the given options.

        Args:
            options (Optional[Options]): Chrome options for the WebDriver.
            use_driver_manger (bool): Flag to use webdriver manager for ChromeDriver.
            driver (Optional[WebDriver]): Existing WebDriver instance.
            logger (Optional[Logger]): Logger instance for logging information.
            use_wire (bool): Flag to use selenium-wire for ChromeDriver.
            wire_options (Optional[dict]): Options for selenium-wire.

        """
        self.options = options
        self.logger: Logger = logger

        if self.options is None:
            self.options = OptionsMode(mode=0, page_load_strategy=0).options

        if self.logger is None:
            self.logger = self._set_logger()

        if driver:
            self.driver = driver
        else:
            if use_driver_manger:
                self.driver = webdriver.Chrome(
                    service=ChromiumService(
                        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
                    ),
                    options=self.options,
                )
            elif use_wire:
                self.driver = wire_driver.Chrome(
                    options=self.options, seleniumwire_options=wire_options
                )
            else:
                self.driver = self.init_driver()

    def init_driver(self) -> webdriver.Chrome:
        """
        Initializes and returns a Chrome WebDriver instance.
        Returns:
            webdriver.Chrome: The initialized Chrome WebDriver instance.
        Raises:
            RuntimeError: If an error occurs while creating the WebDriver instance.
        """
        try:
            driver = webdriver.Chrome(options=self.options)
        except Exception:
            try:
                chromedriver_autoinstaller.install()
                driver = webdriver.Chrome(options=self.options)
            except Exception as exc:
                raise RuntimeError(
                    """ERROR : 
                    - Make sure you're running in the headless mode, headless = True, if you're running on cloud or remotely
                    - Make sure you're passing in `options` attribute from `OptionsMode` class. no the class instance"
                        ```python
                        options = OptionsMode(mode=1, headless=True, maximized=False).options
                        browser = Browser(options=options)
                        ```
                    - Make sure there Chrome browser installed on your machine
                    """
                ) from exc

        self.logger.info("Driver created successfully")
        return driver

    def _set_logger(self) -> Logger:
        """
        Sets up and returns a Logger instance.

        This function creates a Logger instance with the current date as part of the log name.

        Returns:
            Logger: The initialized Logger instance.
        """
        current_time = time.strftime("%Y-%m-%d", time.localtime())
        logs_name = f"SelenEnchanted-{current_time}"

        return Logger(
            log_dir="logs",
            console_logging=True,
            clear_logs=False,
            logs_name=logs_name,
        )
