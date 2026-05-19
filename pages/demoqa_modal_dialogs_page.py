import allure
from playwright.async_api import Page

from base.base_page import BasePage
from config import settings


class DemoqaModalDialogsPage(BasePage):
    """Page object for https://demoqa.com/modal-dialogs."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{settings.DEMOQA_BASE_URL}/modal-dialogs"

    @allure.step("Navigate to Modal Dialogs page")
    async def navigate_to_modal_dialogs(self):
        await self.navigate(self.url)

    @allure.step("Open small modal")
    async def open_small_modal(self):
        await self.page.locator("#showSmallModal").click()
        await self.page.locator("#example-modal-sizes-title-sm").wait_for(state="visible")

    @allure.step("Open large modal")
    async def open_large_modal(self):
        await self.page.locator("#showLargeModal").click()
        await self.page.locator("#example-modal-sizes-title-lg").wait_for(state="visible")

    async def small_modal_body_text(self) -> str:
        return (await self.page.locator(".modal-body").text_content()) or ""

    async def large_modal_body_text(self) -> str:
        return (await self.page.locator(".modal-body").text_content()) or ""

    @allure.step("Close small modal")
    async def close_small_modal(self):
        await self.page.locator("#closeSmallModal").click()

    @allure.step("Close large modal")
    async def close_large_modal(self):
        await self.page.locator("#closeLargeModal").click()
