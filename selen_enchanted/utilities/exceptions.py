class RequestAbuseAlertException(Exception):
    """
    Raised when the system detects an abuse of requests, typically indicated by
    collecting less than 2 posts per page.
    """

    def __init__(self, message="Request abuse alert"):
        self.message = message
        super().__init__(self.message)


class LogOutFailedException(Exception):
    """
    Raised when a login attempt fails, typically due to incorrect account credentials.
    """

    def __init__(self, message="Failed to logout"):
        self.message = message
        super().__init__(self.message)


class LoginFailedException(Exception):
    """
    Raised when a login attempt fails, typically due to incorrect account credentials.
    """

    def __init__(self, message="Failed to login - check the account credentials"):
        self.message = message
        super().__init__(self.message)


class PageAccessiblityException(Exception):
    """
    Raised when a page is not accessible, typically due to the page being removed or
    the account being blocked and the element to enter the page is not found.
    """

    def __init__(self, message="Page Not Accessible - Content Blocked"):
        self.message = message
        super().__init__(self.message)


class ExpectedElementNotFoundException(Exception):
    """
    Raised when an element is not found, typically due to the element not being
    present in the page source.
    """

    def __init__(self, message="Element Not Found - but expected"):
        self.message = message
        super().__init__(self.message)


class StaleElementError(Exception):
    """
    Raised when an element is no longer attached to the DOM, typically due to the
    element being removed from the page source.
    """

    def __init__(
        self, message="Stale Element Error - element no longer attached to the DOM"
    ):
        self.message = message
        super().__init__(self.message)


class CoreClickFailedException(Exception):
    """
    Raised when a click action fails, typically due to the element not being clickable.
    """

    def __init__(self, message="Failed to click on the element"):
        self.message = message
        super().__init__(self.message)


class ScrollFailedException(Exception):
    """
    Raised when a scroll action fails, typically due to the scroll not being executed.
    """

    def __init__(self, message="Failed to scroll"):
        self.message = message
        super().__init__(self.message)


class NoIdException(Exception):
    """
    Exception raised when no free ID is found to use.

    Args:
        message (str, optional): Custom error message. Defaults to "No free ID to use found".
    """

    def __init__(self, message="No free ID to use found"):
        self.message = message
        super().__init__(self.message)


class UnableToFindDateElement(Exception):
    """
    Exception raised when the date element cannot be found.

    Args:
        message (str, optional): Custom error message. Defaults to "Couldn't find the date element".
    """

    def __init__(self, message="Couldn't find the date element"):
        self.message = message
        super().__init__(self.message)


class ExecutionFailedException(Exception):
    """
    Exception raised when an execution fails.

    Args:
        message (str, optional): The error message. Defaults to "Execution failed".
    """

    def __init__(self, message="Execution failed"):
        self.message = message
        super().__init__(self.message)
