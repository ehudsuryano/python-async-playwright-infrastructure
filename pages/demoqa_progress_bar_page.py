import allure
from playwright.async_api import Page, expect

from base.base_page import BasePage
from config import settings


class DemoqaProgressBarPage(BasePage):
    """Page object for https://demoqa.com/progress-bar."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{settings.DEMOQA_BASE_URL}/progress-bar"

    @allure.step("Navigate to Progress Bar page")
    async def navigate_to_progress_bar(self):
        await self.navigate(self.url)

    @allure.step("Start progress")
    async def start(self):
        await self.page.locator("#startStopButton").click()

    @allure.step("Wait until progress reaches 100%")
    async def wait_for_complete(self, timeout_ms: int = 15000):
        await expect(self.page.locator(".progress-bar")).to_have_attribute(
            "aria-valuenow", "100", timeout=timeout_ms
        )

    async def get_value(self) -> str:
        return (await self.page.locator(".progress-bar").get_attribute("aria-valuenow")) or ""

    @allure.step("Reset progress")
    async def reset(self):
        await self.page.locator("#resetButton").click()
