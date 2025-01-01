import asyncio

from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from utilities.logger import get_logger
from base.base_handler import BaseHandler

logger = get_logger()


class TextboxHandler(BaseHandler):
    @staticmethod
    async def get_elements(page: Page, query: str, timeout: int = 10000,**kwargs):
        """
        Wait for and return all web elements matching the query using Playwright's modern locator methods.
        Falls back to the main locator if additional locators fail.

        :param page: Playwright's Page instance
        :param query: String to locate elements (e.g., name, title, or id)
        :param timeout: Maximum time to wait for the elements (default is 10,000 ms)
        :return: List of element handles found using various locator strategies
        """
        logger.debug(f"Searching for elements with query: {query}")

        try:
            # Additional locators
            main_locators = [
                page.get_by_role("textbox", name=query),
                page.get_by_label(query),
                page.get_by_test_id(query),
                page.get_by_placeholder(query)
            ]

            elements = []
            main_succeeded = False

            # Try main locators first
            seen_elements = set()
            short_timeout = timeout // 3  # Shorter timeout for additional locators

            for locator in main_locators:
                try:
                    await locator.wait_for(state="attached", timeout=short_timeout)
                    for handle in await locator.element_handles():
                        try:
                            element_id = f"{await handle.get_attribute('id')}:{await handle.get_attribute('name')}:{await handle.get_attribute('type')}"
                            if element_id not in seen_elements:
                                seen_elements.add(element_id)
                                elements.append(handle)
                        except Exception:
                            elements.append(handle)
                    if elements:
                        logger.debug(f"Found {len(elements)} elements with main locators for query '{query}'.")
                        main_succeeded = True
                        return elements
                except PlaywrightTimeoutError:
                    continue

            if not main_succeeded:
                # Fall back to the additional locator
                additional_locator = page.locator(f"""
                    input[name='{query}'][type='text'],
                    input[name='{query}'][type='password'],
                    input[name='{query}'][type='email'],
                    input[title='{query}'],
                    textarea[name='{query}'],
                    textarea[title='{query}'],
                    #{query},
                    input[placeholder='{query}']
                """)

                try:
                    await additional_locator.wait_for(state="attached", timeout=timeout)
                    elements = await additional_locator.element_handles()
                    if elements:
                        logger.debug(f"Found {len(elements)} elements with additional locators.")
                        return elements
                except PlaywrightTimeoutError:
                    logger.debug("additional locator failed after falling back main locators.")

            return elements

        except Exception as e:
            logger.error(f"Error while searching for elements with query '{query}': {str(e)}")
            return []