# exceptions.py
from typing import Optional
from playwright.async_api import Error as PlaywrightError

class WebElementException(PlaywrightError):  # Inherit from PlaywrightError instead
    """Base exception for web element operations"""

    def __init__(self, message: str, element_info: Optional[dict] = None):
        self.element_info = element_info or {}
        super().__init__(message)


class ElementNotFoundException(WebElementException):
    """Raised when an element cannot be found on the page"""

    def __init__(self, locator: str, timeout: int):
        message = f"Element not found with locator '{locator}' after {timeout}ms"
        super().__init__(message, {"locator": locator, "timeout": timeout})


class ElementNotInteractableException(WebElementException):
    """Raised when an element is found but cannot be interacted with"""

    def __init__(self, locator: str, state: str):
        message = f"Element '{locator}' found but not {state}"
        super().__init__(message, {"locator": locator, "required_state": state})


class ElementStateException(WebElementException):
    """Raised when an element is in an invalid state"""

    def __init__(self, locator: str, expected_state: str, actual_state: str):
        message = f"Element '{locator}' in invalid state. Expected: {expected_state}, Actual: {actual_state}"
        super().__init__(message, {
            "locator": locator,
            "expected_state": expected_state,
            "actual_state": actual_state
        })