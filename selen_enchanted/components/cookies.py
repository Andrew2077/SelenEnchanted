import json
import os

from selenium.webdriver.remote.webdriver import WebDriver


class Cookies:
    """
    A class to manage browser cookies using Selenium WebDriver.

    Attributes:
    ----------
    driver : WebDriver
        The Selenium WebDriver instance used to interact with the browser.

    Methods:
    -------
    save_cookies():
        Saves the current cookies from the browser to a JSON file.

    load_cookies(cookies_path: str):
        Loads cookies from a JSON file and adds them to the browser.

    clear_all_cookies():
        Clears all cookies from the browser.
    """

    def __init__(self, driver: WebDriver):
        """
        Constructs all the necessary attributes for the Cookies object.

        Parameters:
        ----------
        driver : WebDriver
            The Selenium WebDriver instance used to interact with the browser.
        """
        self.driver = driver

    def save_cookies(self, name: str = "cookies"):
        """
        Save the cookies from the current Selenium WebDriver session to a JSON file.

        Args:
            name (str, optional): The name of the JSON file to save the cookies to. Defaults to "cookies".
        """
        directory = "./configs/cookies/"
        filename = f"{name}.json"
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, filename)
        with open(path, "w") as file:
            json.dump(self.driver.get_cookies(), file)

    def load_cookies(self, cookies_path: str):
        """
        Loads cookies from a JSON file and adds them to the browser.

        Parameters:
        ----------
        cookies_path : str
            The path to the JSON file containing the cookies.
        """
        with open(cookies_path, "r") as file:
            cookies = json.load(file)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

    def clear_all_cookies(self):
        """
        Clears all cookies from the browser.

        This method deletes all cookies from the browser and refreshes the page.
        """
        self.driver.delete_all_cookies()
        self.driver.refresh()
