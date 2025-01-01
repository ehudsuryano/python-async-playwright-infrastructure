from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from utilities.logger import get_logger
from base.base_handler import BaseHandler

logger = get_logger()


class SideMenuItemHandler(BaseHandler):
    @staticmethod
    async def get_elements(page: Page, item_name: str, timeout: int = 10000, **kwargs):
        """
        Wait for and return all web elements matching the query using Playwright's modern locator methods.
        Optimized for performance while maintaining reliability.

        :param page: Playwright's Page instance
        :param item_name: String to locate elements (e.g., name, title, or id)
        :param timeout: Maximum time to wait for the elements (default is 10,000 ms)
        :return: List of element handles found using various locator strategies
        """
        logger.debug(f"Searching for elements with query: {item_name}")

        try:
            # Combine most common selectors into a single locator for better performance
            main_locator = page.get_by_text(item_name)

            # Try the combined selector first with the full timeout
            try:
                await main_locator.wait_for(state="attached", timeout=timeout)
                elements = await main_locator.element_handles()
                if elements:
                    logger.debug(f"Found {len(elements)} elements with main locator {item_name}.")
                    return elements
            except PlaywrightTimeoutError:
                pass

            # If main locator fails, try these additional locators with a shorter timeout
            additional_locators = [
                page.get_by_role("textbox", name=item_name),
                page.get_by_label(item_name),
                page.get_by_test_id(item_name)
            ]

            elements = []
            seen_elements = set()
            short_timeout = timeout // 3  # Shorter timeout for additional locators

            for locator in additional_locators:
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
                except PlaywrightTimeoutError:
                    continue

            logger.debug(f"Found {len(elements)} total unique elements matching query '{item_name}'.")
            return elements

        except PlaywrightTimeoutError as e:
            logger.error(f"Error while searching for elements with query '{item_name}': {str(e)}")
            return []