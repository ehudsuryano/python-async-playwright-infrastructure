import asyncio

from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from utilities.logger import get_logger
from base.base_handler import BaseHandler

logger = get_logger()


class TextboxHandler(BaseHandler):
    @staticmethod
    async def get_elements(page: Page, query: str, timeout: int = 10000, **kwargs):
        """
        Simplified version optimized for performance by reducing async overhead.
        """
        logger.debug(f"Searching for elements with query: {query}")

        try:
            # Use a single locator that combines all selectors
            combined_locator = page.locator(f"""
                [role='textbox'][name='{query}'],
                [aria-label='{query}'],
                [data-testid='{query}'],
                [placeholder='{query}'],
                input[name='{query}'][type='text'],
                input[name='{query}'][type='password'],
                input[name='{query}'][type='email'],
                input[title='{query}'],
                textarea[name='{query}'],
                textarea[title='{query}'],
                #{query}
            """)

            await combined_locator.wait_for(state="attached", timeout=timeout)
            elements = await combined_locator.element_handles()

            logger.debug(f"Found {len(elements)} elements")
            return elements

        except Exception as e:
            logger.error(f"Error searching for elements: {str(e)}")
            return []