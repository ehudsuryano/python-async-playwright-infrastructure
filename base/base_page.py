class BasePage:
    def __init__(self, page):
        self.page = page

    async def navigate(self, url: str):
        await self.page.goto(url)

    async def get_title(self) -> str:
        return await self.page.title()

    async def get_url(self) -> str:
        """
        Returns the current URL of the browser.
        Returns:
            str: The current URL of the page
        """
        return self.page.url

    async def is_element_exist(self, selector: str):
        """
        Checks if an element exists on the page.

        :param selector: CSS or XPath selector for the element
        :return: True if the element exists, False otherwise
        """
        return await self.page.locator(selector).count() > 0