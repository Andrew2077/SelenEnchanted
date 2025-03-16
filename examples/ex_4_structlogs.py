from selen_enchanted import Browser, Logger

logger = Logger(use_structlog=True, logs_name="TestApp")
browser = Browser(logger=logger)
browser.get_url("https://www.google.com")
browser.wait(5)

logger.info("it works")
logger.error("it doesn't work")
logger.warning("it might work")
logger.debug("it might not work")
logger.critical("it might not work")

browser.close()

