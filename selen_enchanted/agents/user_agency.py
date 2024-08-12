"""
user_agency.py

This module provides a UserAgentGenerator class to generate user agent strings and client hints for different platforms, browsers, and devices.
"""

import random
import ua_generator
from ua_generator.user_agent import UserAgent

from typing import Tuple, Union, Optional
from user_agents import parse
from .info import OLD_EMULATOR, ios_models


class UserAgentGenerator:
    """
    A class to generate user agent strings and client hints for different platforms, browsers, and devices.

    Attributes:
        device (Union[Tuple, str]): The type of device (e.g., "mobile").
        platform (Union[Tuple, str]): The platform (e.g., "android").
        browser (Union[Tuple, str]): The browser (e.g., "chrome").
        min_version (int): The minimum version of the browser.
        max_version (int): The maximum version of the browser.
        width (int): The width of the device screen.
        height (int): The height of the device screen.
        pixel_ratio (float): The pixel ratio of the device screen.
        ua (Optional[UserAgent]): The generated user agent.
        client_hints (Optional[dict]): The generated client hints.
        emulation (dict): The generated emulation settings.
    """

    def __init__(
        self,
        platform: Union[Tuple, str] = ("android"),
        browser: Union[Tuple, str] = "chrome",
        device: Union[Tuple, str] = "mobile",
        min_version: int = 120,
        max_version: int = 125,
        load_old_exp: bool = False,
    ):
        """
        Initializes the UserAgentGenerator with the specified parameters.

        Args:
            platform (Union[Tuple, str]): The platform (default is "android").
            browser (Union[Tuple, str]): The browser (default is "chrome").
            device (Union[Tuple, str]): The device type (default is "mobile").
            min_version (int): The minimum version of the browser (default is 120).
            max_version (int): The maximum version of the browser (default is 125).
            load_old_exp (bool): Whether to load old emulation settings (default is False).
        """
        self.device = device
        self.platform = platform
        self.browser = browser
        self.min_version = min_version
        self.max_version = max_version

        self.width = random.randint(400, 500)
        self.height = random.randint(640, 900)
        self.pixel_ratio = round(random.uniform(1.5, 3.5), 2)

        self.ua: Optional[UserAgent] = None
        self.client_hints: Optional[dict] = None
        self.emulation = self.generate(load_old_exp)

    def _get_chrome_version(self, ua_text: str) -> Tuple[str, str]:
        """
        Extracts the Chrome version from the user agent string.

        Args:
            ua_text (str): The user agent string.

        Returns:
            Tuple[str, str]: The major version and full version of the Chrome browser.
        """
        ua = parse(ua_text)
        return ua.browser.version_string.split(".")[0], ua.browser.version_string

    def _generate_ua(self) -> None:
        """
        Generates a user agent string that matches the specified criteria.
        """
        keep_searching = True
        while keep_searching:
            ua = ua_generator.generate(
                device=self.device, platform=self.platform, browser=self.browser
            )
            user_agent = ua.text
            version, _ = self._get_chrome_version(user_agent)
            if int(version) >= self.min_version and int(version) <= self.max_version:
                self.ua = ua
                keep_searching = False

    def _gen_brand_and_model(self) -> Tuple[str, str]:
        """
        Generates the brand and model of the device based on the user agent string.

        Returns:
            Tuple[str, str]: The brand and model of the device.
        """
        parsed = parse(self.ua.text)
        if parsed.device.brand == "Samsung":
            return parsed.device.brand, parsed.device.model

        elif parsed.device.brand == "Apple" and parsed.device.model == "iPhone":
            return parsed.device.brand, random.choice(ios_models)
        else:
            return parsed.device.brand, parsed.device.model

    def _create_clienthints(self) -> None:
        """
        Creates client hints based on the generated user agent string.
        """
        version, full_version = self._get_chrome_version(self.ua.text)
        brand, model = self._gen_brand_and_model()
        self.client_hints = {
            "brands": [
                {"brand": "Google Chrome", "version": version},
                {"brand": "Chromium", "version": version},
            ],
            "fullVersionList": [
                {"brand": "Google Chrome", "version": full_version},
                {"brand": "Chromium", "version": full_version},
            ],
            "platform": str(self.ua.ch.platform[1:-1]),
            "platformVersion": str(self.ua.ch.platform_version[1:-1]),
            "architecture": str(self.ua.ch.architecture[1:-1]),
            "model": model,
            "mobile": True,
            "bitness": str(self.ua.ch.bitness[1:-1]),
            "wow64": False,
        }

    def create_emulation(self) -> dict:
        """
        Creates emulation settings based on the generated user agent and client hints.

        Returns:
            dict: The emulation settings.
        """
        return {
            "userAgent": self.ua.text,
            "deviceMetrics": {
                "mobile": True,
                "touch": True,
                "width": self.width,
                "height": self.height,
                "pixelRatio": self.pixel_ratio,
            },
            "clientHints": self.client_hints,
        }

    def generate(self, load_old: bool = False) -> dict:
        """
        Generates the emulation settings.

        Args:
            load_old (bool): Whether to load old emulation settings (default is False).

        Returns:
            dict: The generated emulation settings.
        """
        if load_old:
            return OLD_EMULATOR
        self._generate_ua()
        self._create_clienthints()
        emulation = self.create_emulation()
        return emulation

    def __call__(self):
        """
        Returns the generated emulation settings when the instance is called.

        Returns:
            dict: The generated emulation settings.
        """
        return self.emulation


if __name__ == "__main__":
    ua = UserAgentGenerator()
    emulation = ua()  # ua.emulation
