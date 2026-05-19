import allure
from playwright.async_api import Page

from base.base_page import BasePage
from config import settings


class DemoqaBrowserWindowsPage(BasePage):
    """Page object for https://demoqa.com/browser-windows."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{settings.DEMOQA_BASE_URL}/browser-windows"

    @allure.step("Navigate to Browser Windows page")
    async def navigate_to_browser_windows(self):
        await self.navigate(self.url)

    async def _open_via(self, button_id: str) -> Page:
        async with self.page.context.expect_page() as new_page_info:
            await self.page.locator(button_id).click()
        new_page = await new_page_info.value
        await new_page.wait_for_load_state("domcontentloaded")
        return new_page

    @allure.step("Open new tab")
    async def open_new_tab(self) -> Page:
        return await self._open_via("#tabButton")

    @allure.step("Open new window")
    async def open_new_window(self) -> Page:
        return await self._open_via("#windowButton")
