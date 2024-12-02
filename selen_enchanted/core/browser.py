from typing import Optional, Union, List, Dict

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from ..core.driver import ChromeDriver
from ..core.javascripts import JavaScripts
from ..components.actions import Actions
from ..components.locator import Locator
from ..components.scroller import Scroller
from ..components.tab import Tab
from ..components.cookies import Cookies
from ..utilities.logger import Logger
from ..utilities.profiler import Profiler
from ..utilities.sleeper import Sleeper


class Browser:
    """
    The Browser class facilitates interaction with web pages using Selenium WebDriver, serving as a comprehensive wrapper around the WebDriver.

    Key Features:
    - Direct access to all WebDriver actions via the `driver` attribute.
    - Default options are applied if no specific options are provided. Refer to `options.py` for detailed documentation on option modes.
    - Automatic installation of ChromeDriver using `chromedriver_autoinstaller` if not already present.
    - Optional use of ChromeDriverManager for ChromeDriver installation by setting `use_driver_manager` to True.
    - Support for selenium-wire with customizable proxy settings through `wire_options`.
        - Example configuration:
        ```python
        wire_options = {
            "proxy": {
                "http": "http://localhost:8888",
                "https": "http://localhost:8888",
            }
        }
        ```
    - For additional selenium-wire configuration options, visit: https://github.com/wkeeling/selenium-wire
    """

    def __init__(
        self,
        options: Optional[Options] = None,
        use_driver_manger: bool = False,
        driver: Optional[WebDriver] = None,
        logger: Optional[Logger] = None,
        use_wire: bool = False,
        wire_options: Optional[dict] = None,
    ):
        self.web_driver = ChromeDriver(
            options=options,
            use_driver_manger=use_driver_manger,
            driver=driver,
            logger=logger,
            use_wire=use_wire,
            wire_options=wire_options,
        )
        self.driver = self.web_driver.driver
        self.logger = self.web_driver.logger
        self.sleeper = Sleeper()
        self.tab = Tab(self.driver, self.logger)
        self.locator = Locator(self.driver, self.logger)
        self.actions = Actions(self.driver, self.logger)
        self.scroller = Scroller(self.driver)
        self.cookies = Cookies(self.driver)
        self.js = JavaScripts

        # Selenium objects
        self.Keys = Keys()
        self.By = By
        self.ActionChains = ActionChains

        # Profile
        self.profile = Profiler()

    def wait(self, seconds: int):
        """For detailed DocString use `help(Browser.wait)` or use `browser.sleeper.wait`"""
        self.sleeper.wait(seconds)

    def wait_random_time(self, min_duration: int, max_duration: int):
        """For detailed DocString use `help(Browser.wait_random_time)` or use `browser.sleeper.wait_random_time`"""
        self.sleeper.wait_random_time(min_duration, max_duration)

    def catigorized_fixed_wait(self, duration: str):
        """For detailed DocString use `help(Browser.catigorized_fixed_wait)` or use `browser.sleeper.catigorized_fixed_wait`"""
        self.sleeper.catigorized_fixed_wait(duration)

    def catigorized_random_wait(
        self, duration: str, custom_duration: Optional[tuple[int, int]] = None
    ):
        """For detailed DocString use `help(Browser.catigorized_random_wait)` or use `browser.sleeper.catigorized_random_wait`"""
        self.sleeper.catigorized_random_wait(duration, custom_duration)

    def get_url(self, url: str, remove_translation: bool = True):
        """For detailed DocString use `help(Browser.get_url)` or use `browser.tab.get_url`"""
        self.tab.get_url(url, remove_translation=remove_translation)

    def get(self, url: str):
        """For detailed DocString use `help(Browser.get)` or use `browser.tab.get`"""
        self.tab.get(url)

    def open_new_window(self, url):
        """For detailed DocString use `help(Browser.open_new_window)` or use `browser.tab.open_new_window`"""
        self.tab.open_new_window(url)

    def switch_window(self, window_number: int):
        """For detailed DocString use `help(Browser.switch_window)` or use `browser.tab.switch_window`"""
        self.tab.switch_window(window_number)

    def close_last_opened_window(self):
        """For detailed DocString use `help(Browser.close_last_opened_window)` or use `browser.tab.close_last_opened_window`"""
        self.tab.close_last_opened_window()

    def back_url(self):
        """For detailed DocString use `help(Browser.back_url)` or use `browser.tab.back_url`"""
        self.tab.back_url()

    def close(self, timeout: int = 2):
        """For detailed DocString use `help(Browser.close)` or use `browser.tab.close`"""
        self.tab.close(timeout=timeout)

    def screen(self, name: str = "test"):
        """For detailed DocString use `help(Browser.screen)` or use `browser.tab.screen`"""
        self.tab.screen(name=name)

    def save_image(self, url: str, path: str):
        """For detailed DocString use `help(Browser.save_image)` or use `browser.tab.save_image`"""
        self.tab.save_image(url, path)

    def save_base64_image(self, base64_image: str, path: str):
        """For detailed DocString use `help(Browser.save_base64_image)` or use `browser.tab.save_base64_image`"""
        self.tab.save_base64_image(base64_image, path)

    def download_content(self, src: str, path: str, name: str):
        """For detailed DocString use `help(Browser.download_content)` or use `browser.tab.download_content`"""
        self.tab.download_content(src, path, name)

    def find_element(
        self,
        method: By,
        val: str,
        parent: Optional[WebElement] = None,
        timeout: int = 5,
    ) -> WebElement:
        """For detailed DocString use `help(Browser.find_element)` or use `browser.locator.find_element`"""
        return self.locator.find_element(method, val, parent, timeout)

    def find_elements(
        self,
        method: By = By.XPATH,
        val: str = None,
        parent: Optional[WebElement] = None,
        timeout: int = 5,
    ) -> list[WebElement]:
        """For detailed DocString use `help(Browser.find_elements)` or use `browser.locator.find_elements`"""
        return self.locator.find_elements(method, val, parent, timeout)

    def click_on(self, x_coord: int, y_coord: int, delay: int = 1):
        """For detailed DocString use `help(Browser.click_on)` or use `browser.actions.click_on`"""
        self.actions.click_on(x_coord, y_coord, delay)

    def press_esc(self):
        """For detailed DocString use `help(Browser.press_esc)` or use `browser.actions.press_esc`"""
        self.actions.press_esc()

    def press_key(self, key: str):
        """For detailed DocString use `help(Browser.press_key)` or use `browser.actions.press_key`"""
        self.actions.press_key(key)

    def click_by_mouse(self, element: WebElement, num_clicks: int = 1):
        """For detailed DocString use `help(Browser.click_by_mouse)` or use `browser.actions.click_by_mouse`"""
        self.actions.click_by_mouse(element, num_clicks)

    def calc_element_center(self, element: WebElement) -> tuple[int, int]:
        """For detailed DocString use `help(Browser.calc_element_center)` or use `browser.actions.calc_element_center`"""
        return self.actions.calc_element_center(element)

    def click_on_location(self, x: int, y: int):
        """For detailed DocString use `help(Browser.click_on_location)` or use `browser.actions.click_on_location`"""
        self.actions.click_on_location(x, y)

    def highlight_element(self, element: WebElement):
        """For detailed DocString use `help(Browser.highlight_element)` or use `browser.actions.highlight_element`"""
        self.actions.highlight_element(element)

    def mark_current_position_with_dot(self):
        """For detailed DocString use `help(Browser.mark_current_position_with_dot)` or use `browser.actions.mark_current_position_with_dot`"""
        self.actions.mark_current_position_with_dot()

    def get_current_cursor_coords(self) -> tuple[int, int]:
        """For detailed DocString use `help(Browser.get_current_cursor_coords)` or use `browser.actions.get_current_cursor_coords`"""
        return self.actions.get_current_cursor_coords()

    def hover(self, element: WebElement, timeout: Union[str, int] = "very_short"):
        """For detailed DocString use `help(Browser.hover)` or use `browser.actions.hover`"""
        self.actions.hover(element, timeout)

    def hover_over_coordinates(self, x: int, y: int, click: bool = False):
        """For detailed DocString use `help(Browser.hover_over_coordinates)` or use `browser.actions.hover_over_coordinates`"""
        self.actions.hover_over_coordinates(x, y, click)

    def move_cursor_and_mark(self, x: int, y: int):
        """For detailed DocString use `help(Browser.move_cursor_and_mark)` or use `browser.actions.move_cursor_and_mark`"""
        self.actions.move_cursor_and_mark(x, y)

    def ensure_transition(self):
        """For detailed DocString use `help(Browser.ensure_transition)` or use `browser.actions.ensure_transition`"""
        self.actions.ensure_transition()

    def clear_input(self, input_element: WebElement):
        """For detailed DocString use `help(Browser.clear_input)` or use `browser.actions.clear_input`"""
        self.actions.clear_input(input_element)

    def send_keys_letter_by_letter(self, element: WebElement, data: str):
        """For detailed DocString use `help(Browser.send_keys_letter_by_letter)` or use `browser.actions.send_keys_letter_by_letter`"""
        self.actions.send_keys_letter_by_letter(element, data)

    def scroll_element(self, element: WebElement):
        """For detailed DocString use `help(Browser.scroll_element)` or use `browser.scroller.scroll_element`"""
        self.scroller.scroll_element(element)

    def scroll_page(self, length: int):
        """For detailed DocString use `help(Browser.scroll_page)` or use `browser.scroller.scroll_page`"""
        self.scroller.scroll_page(length)

    def scroll_to_element(self, element: WebElement):
        """For detailed DocString use `help(Browser.scroll_to_element)` or use `browser.scroller.scroll_to_element`"""
        self.scroller.scroll_to_element(element)

    def scroll_like_mouse(
        self,
        scroll_length: tuple[int, int] = (35, 120),
        scrolls_count: int = None,
        timeout: float = 0.03,
    ):
        """For detailed DocString use `help(Browser.scroll_like_mouse)` or use `browser.scroller.scroll_like_mouse`"""
        self.scroller.scroll_like_mouse(scroll_length, scrolls_count, timeout)

    def scroll_like_mouse_to_element(
        self,
        element: WebElement,
        scroll_length: tuple[int, int] = (35, 120),
        timeout: float = 0.03,
        tolerance: float = 0.7,
    ):
        """For detailed DocString use `help(Browser.scroll_like_mouse_to_element)` or use `browser.scroller.scroll_like_mouse_to_element`"""
        self.scroller.scroll_like_mouse_to_element(
            element, scroll_length, timeout, tolerance
        )

    def save_cookies(self, name: str = "cookies"):
        """For detailed DocString use `help(Browser.save_cookies)` or use `browser.cookies.save_cookies`"""
        self.cookies.save_cookies(name)

    def load_cookies(self, cookies_path: str):
        """For detailed DocString use `help(Browser.load_cookies)` or use `browser.cookies.load_cookies`"""
        self.cookies.load_cookies(cookies_path)

    def clear_all_cookies(self):
        """For detailed DocString use `help(Browser.clear_all_cookies)` or use `browser.cookies.clear_all_cookies`"""
        self.cookies.clear_all_cookies()

    def save_cookies(self, name: str = "cookies", directory: str = None):
        """For detailed DocString use `help(Browser.save_cookies)` or use `browser.cookies.save_cookies`"""
        self.cookies.save_cookies(name, directory)

    def load_cookies(self, cookies: List[Dict]):
        """For detailed DocString use `help(Browser.load_cookies)` or use `browser.cookies.load_cookies`"""
        self.cookies.load_cookies(cookies)

    def load_cookies_from_path(self, cookies_path: str):
        """For detailed DocString use `help(Browser.load_cookies_from_path)` or use `browser.cookies.load_cookies_from_path`"""
        self.cookies.load_cookies_from_path(cookies_path)
