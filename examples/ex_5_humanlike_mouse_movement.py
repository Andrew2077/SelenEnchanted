from selen_enchanted import Browser
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selen_enchanted.components.actions import Actions
from selen_enchanted.utilities.logger import Logger
from selen_enchanted.components.scroller import Scroller


logger = Logger(use_structlog=True, logs_name="TestApp")
browser = Browser()
browser.get_url("https://www.w3schools.com/howto/default.asp")
browser.wait(5)
browser.driver.maximize_window()
actions = Actions(browser.driver, logger)
scroller = Scroller(browser.driver)
button = browser.find_element(By.XPATH, "//a[@href='/spaces/index.php']")
# simulate move & click
actions.click_by_mouse(button)
time.sleep(3)

button = browser.find_element(By.XPATH, '//a[@href="/academy/index.php"]')
# simulate move & click
actions.click_by_mouse(button)
time.sleep(3)


scroller.scroll_like_mouse(scrolls_count=10)

button = browser.find_element(By.XPATH, '//a[@href="https://webinars.w3schools.com/webinar/w3schools-academy-for-educators-17442?session=replay&showform=1%3Fsession%3Dreplay&showform=1"]')
# simulate move & click
actions.click_by_mouse(button)
time.sleep(20)

# scroller.scroll_like_mouse(scrolls_count=10)
# button = browser.find_element(By.XPATH, '//a[contains(@href,"/explore/topics/")]')
# actions.click_by_mouse(button)
# time.sleep(20)