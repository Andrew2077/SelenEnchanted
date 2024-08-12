from selen_enchanted import Browser, OptionsMode

options = OptionsMode().options
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--headless")

browser = Browser(options=options)
browser.get_url("https://www.google.com")
browser.wait(5)
