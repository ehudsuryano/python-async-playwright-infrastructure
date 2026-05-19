import allure
from playwright.async_api import Page

from base.base_page import BasePage
from config import settings


class DemoqaTabsPage(BasePage):
    """Page object for https://demoqa.com/tabs."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{settings.DEMOQA_BASE_URL}/tabs"

    @allure.step("Navigate to Tabs page")
    async def navigate_to_tabs(self):
        await self.navigate(self.url)

    @allure.step("Open tab '{tab}'")
    async def open_tab(self, tab: str):
        await self.page.locator(f"#demo-tab-{tab}").click()

    async def panel_text(self, tab: str) -> str:
        return (await self.page.locator(f"#demo-tabpane-{tab}").text_content()) or ""

    async def is_tab_disabled(self, tab: str) -> bool:
        klass = await self.page.locator(f"#demo-tab-{tab}").get_attribute("class") or ""
        aria_disabled = await self.page.locator(f"#demo-tab-{tab}").get_attribute("aria-disabled") or ""
        return "disabled" in klass or aria_disabled.lower() == "true"
