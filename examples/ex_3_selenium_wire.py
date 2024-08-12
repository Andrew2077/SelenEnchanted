from selen_enchanted import Browser, OptionsMode

PROXY = "http://{username}:{password}@{host}:{port}".format(
    username="username", password="password", host="host", port="port"
)

selenium_wire_options = {
    "disable_encoding": False,
    "disable_capture": True,
    "proxy": {"http": PROXY, "https": PROXY, "no_proxy": "localhost,127.0.0.1"},
}

options = OptionsMode(mode=1, headless=False, maximized=False).options
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")

browser = Browser(options=options, use_wire=True, wire_options=selenium_wire_options)
browser.get_url("https://www.google.com")
browser.wait(5)

