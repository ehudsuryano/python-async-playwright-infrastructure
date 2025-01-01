from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from utilities.logger import get_logger

logger = get_logger()


class BaseHandler:
    def __init__(self, page):
        self.page = page

    async def get_elements(self,page, card_name: str, timeout: int = 10000):
        raise NotImplementedError("The 'load' method must be overridden in the child class.")
