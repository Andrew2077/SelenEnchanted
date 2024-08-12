from selen_enchanted import Browser

browser = Browser()
browser.get_url("https://www.google.com")
browser.wait(5)
