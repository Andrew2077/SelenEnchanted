from selen_enchanted import Browser, OptionsMode

# Create browser with performance logging enabled
options = OptionsMode(mode=1, headless=False, maximized=False, enable_logging=True).options
browser = Browser(options=options)

# Setup listener
listener = browser.listener
listener.set_url_contains_list(["/graphql", "/content"])  # More common API patterns
# listener.set_url_matches_list(["https://www.awwwards.com/sites/hubble/content"])

# Setup network capture before navigating
capture = listener.setup_network_capture()

print("Navigating to website...")
browser.get_url("https://www.awwwards.com/websites/graphql/")

# Wait for page to load and network requests to complete
browser.wait(3)

print("Capturing network requests...")
requests = capture()

print(f"Captured {len(requests)} network requests:")
for i, request in enumerate(requests):
    print(f"{i+1}. {request.get('method', 'GET')} {request.get('url', 'Unknown URL')}")
    print(f"   Status: {request.get('status', 'Unknown')}")
    if request.get('body'):
        body_preview = str(request['body'])[:100] + "..." if len(str(request['body'])) > 100 else str(request['body'])
        print(f"   Body preview: {body_preview}")
    print()

browser.close()
