import allure
from playwright.async_api import Page

from base.base_page import BasePage
from config import settings


class DemoqaTooltipsPage(BasePage):
    """Page object for https://demoqa.com/tool-tips."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{settings.DEMOQA_BASE_URL}/tool-tips"

    @allure.step("Navigate to Tool Tips page")
    async def navigate_to_tooltips(self):
        await self.navigate(self.url)

    @allure.step("Hover button and read tooltip")
    async def hover_button_tooltip(self) -> str:
        await self.page.locator("#toolTipButton").hover()
        tooltip = self.page.locator(".tooltip-inner")
        await tooltip.wait_for(state="visible")
        return (await tooltip.text_content()) or ""

    @allure.step("Hover text field and read tooltip")
    async def hover_textfield_tooltip(self) -> str:
        await self.page.locator("#toolTipTextField").hover()
        tooltip = self.page.locator(".tooltip-inner")
        await tooltip.wait_for(state="visible")
        return (await tooltip.text_content()) or ""
