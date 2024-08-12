"""
This module provides the OptionsMode class for configuring Selenium WebDriver Chrome options.

The OptionsMode class allows users to configure various browser options such as headless mode, incognito mode,
profile directory, window maximization, traffic reduction, and mobile emulation. It also supports different
page load strategies and modes for the browser.

Classes:
    OptionsMode: A class to configure and manage Selenium WebDriver Chrome options.

Constants:
    PLS: A dictionary mapping page load strategy identifiers to their corresponding strategy names.
    MODES: A dictionary mapping mode identifiers to their corresponding mode names.
"""

import os
from typing import Any, Optional

from selenium.webdriver.chrome.options import Options

from ..agents.user_agency import UserAgentGenerator

PLS = {
    0: "normal",  # Used by default by browser and Selenium WebDriver. Waits for all the resources to be downloaded.
    1: "eager",  # Resources like images and CSS might still be loading, but DOM is accessible and ready to interact.
    2: "none",  # WebDriver is not blocked at all. Execution continues without any wait as soon as the initial page is loaded.
}

MODES = {
    0: "default",  # Default mode no arguments are added except for the the ones added to constructor
    1: "base",  # Base mode adds the basic arguments to the browser
    2: "mobile",  # Mobile mode adds the mobile emulation arguments to the browser
}


class OptionsMode:
    """
    A class to configure and manage Selenium WebDriver Chrome options.

    This class allows users to set various options for the Chrome browser, including headless mode, incognito mode,
    profile directory, window maximization, traffic reduction, and mobile emulation. It also supports different
    page load strategies and modes for the browser.

    Attributes:
        options (Options): The Chrome options object, which stores the configured options and can be modified further if needed.
        mode (str): The mode for the browser options.
        pls (str): The page load strategy for the browser.
        emulation (dict): The user agent emulation settings.

    Methods:
        __call__(): Returns the configured Chrome options.
        apply_mode(): Applies the selected mode to the browser options.
        base_mode(): Sets the base mode for the browser options.
        mobile_mode(): Enables mobile mode for the browser.
        reduce_traffic(): Reduces network traffic by disabling extensions and images.
    """

    def __init__(
        self,
        mode: Optional[int] = 0,
        headless: bool = False,
        incognito: bool = False,
        profile_dir: Optional[str] = None,
        maximized: bool = False,
        reduce_traffic: bool = False,
        page_load_strategy: int = 0,
        useragent_emulation: Optional[dict] = None,
    ) -> None:
        """
        Initializes the OptionsMode object with the specified settings.

        Args:
            mode (Optional[int]): The mode for the browser options. Defaults to 0 (default mode).
            headless (bool): Whether to run the browser in headless mode. Defaults to False.
            incognito (bool): Whether to run the browser in incognito mode. Defaults to False.
            profile_dir (Optional[str]): The directory for the browser profile. Defaults to None.
            maximized (bool): Whether to start the browser maximized. Defaults to False.
            reduce_traffic (bool): Whether to reduce network traffic. Defaults to False.
            page_load_strategy (int): The page load strategy for the browser. Defaults to 0 (normal).
            useragent_emulation (Optional[dict]): The user agent emulation settings. Defaults to None.

        Available Modes:
            - 0 (default): Default mode no arguments are added except for the the ones added to constructor
            - 1 (base): Base mode adds the basic arguments to the browser
            - 2 (mobile): Mobile mode adds the mobile emulation arguments to the browser [deaulted to emulated Android device]

        Page Load Strategies:
            - 0 (normal): Used by default by browser and Selenium WebDriver. Waits for all the resources to be downloaded.
            - 1 (eager): Resources like images and CSS might still be loading, but DOM is accessible and ready to interact.
            - 2 (none): WebDriver is not blocked at all. Execution continues without any wait as soon as the initial page is loaded.


        Raises:
            ValueError: If an invalid mode or page load strategy is provided.
        """
        self.options = Options()

        if mode not in MODES:
            raise ValueError("Invalid mode")

        if page_load_strategy not in PLS:
            raise ValueError("Invalid page load strategy")

        self.mode = MODES[mode]
        self.pls = PLS[page_load_strategy]
        self.emulation = useragent_emulation
        self.options.page_load_strategy = self.pls

        self.apply_mode()

        if os.name == "nt":
            self.options.add_argument("--disable-gpu")

        if headless:
            self.options.add_argument("--headless")

        if incognito:
            self.options.add_argument("--incognito")

        if profile_dir:
            self.options.add_argument(f"--user-data-dir={profile_dir}")

        if maximized:
            self.options.add_argument("--start-maximized")

        if reduce_traffic:
            self.reduce_traffic()

    def __call__(self) -> Any:
        """
        Returns the configured Chrome options.

        Returns:
            Options: The configured Chrome options.
        """
        return self.options

    def apply_mode(self):
        """
        Applies the selected mode to the browser options.

        This method sets the necessary arguments and options based on the selected mode.
        """
        if self.mode == "default":
            pass

        elif self.mode == "base":
            self.base_mode()

        elif self.mode == "mobile":
            self.base_mode()
            self.mobile_mode()

    def base_mode(self):
        """
        Sets the base mode for the browser options.

        This method adds various arguments and options to the browser options object to configure the browser in a specific mode.

        Arguments:
        - --ignore-certificate-errors: Ignores certificate errors.
        - --test-type: Sets the browser in test mode.
        - --disable-notifications: Disables browser notifications.
        - --verbose: Enables verbose logging.
        - --no-sandbox: Disables the sandbox for the browser.
        - --disable-dev-shm-usage: Disables the use of /dev/shm.
        - --lang=en-US: Sets the language of the browser to English (United States).
        - --mute-audio: Mutes audio in the browser.
        - --hide-crash-restore-bubble: Hides the crash restore bubble.
        - --crash-dumps-dir=/tmp: Sets the directory for crash dumps to /tmp.
        - --log-level=1: Sets the log level to 1.

        Experimental Options:
        - prefs: Sets the preferences for the browser.
            - intl.accept_languages: Sets the accepted languages to English and English (United States).
        """
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--test-type")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--verbose")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--lang=en-US")
        self.options.add_experimental_option(
            "prefs", {"intl.accept_languages": "en,en_US"}
        )
        self.options.add_argument("--mute-audio")
        self.options.add_argument("--hide-crash-restore-bubble")
        self.options.add_argument("--crash-dumps-dir=/tmp")
        self.options.add_argument("--log-level=1")

    def mobile_mode(self):
        """
        Enables mobile mode for the browser.

        This method sets up the necessary options and arguments to simulate a mobile device in the browser.
        It disables extensions and sets the window size to match the device metrics.

        Returns:
            None
        """
        if not self.emulation:
            self.emulation = UserAgentGenerator().emulation
        self.options.add_argument("--disable-extensions")
        self.options.add_argument(
            f"--window-size={self.emulation['deviceMetrics']['width']},{self.emulation['deviceMetrics']['height']}"
        )

    def reduce_traffic(self):
        """
        Reduces traffic (network overhead) by disabling extensions, setting autoplay policy to 'no-user-gesture-required',
        and disabling images in the browser.
        """
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--autoplay-policy=no-user-gesture-required")
        self.options.add_argument("--blink-settings=imagesEnabled=false")


if __name__ == "__main__":
    options = OptionsMode(mode=0, page_load_strategy=0).options
