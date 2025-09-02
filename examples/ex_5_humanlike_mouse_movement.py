from selen_enchanted import Browser
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selen_enchanted.components.actions import Actions
from selen_enchanted.utilities.logger import Logger

logger = Logger(use_structlog=True, logs_name="TestApp")
browser = Browser()
browser.get_url("https://www.w3schools.com/howto/howto_css_login_form.asp")
browser.wait(5)
browser.driver.maximize_window()
actions = Actions(browser.driver, logger)

button = browser.find_element(By.XPATH, "//a[@href='/spaces/index.php']")
# simulate move & click
actions.click_by_mouse(button)
time.sleep(3)

button = browser.find_element(By.XPATH, '//a[@href="/academy/index.php"]')
# simulate move & click
actions.click_by_mouse(button)
time.sleep(3)

button = browser.find_element(By.XPATH, '//a[@href="https://order.w3schools.com/academy/self-service/"]')
# simulate move & click
actions.click_by_mouse(button)
time.sleep(3)

browser.close()


