import allure
from playwright.async_api import Page

from base.base_page import BasePage
from config import settings


class DemoqaSelectMenuPage(BasePage):
    """Page object for https://demoqa.com/select-menu."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{settings.DEMOQA_BASE_URL}/select-menu"

    @allure.step("Navigate to Select Menu page")
    async def navigate_to_select_menu(self):
        await self.navigate(self.url)

    @allure.step("Pick '{option}' in 'Select Value'")
    async def pick_select_value(self, option: str):
        await self.page.locator("#withOptGroup").click()
        await self.page.get_by_text(option, exact=True).first.click()

    async def get_selected_value(self) -> str:
        return (await self.page.locator('#withOptGroup [class*="singleValue"]').text_content()) or ""

    @allure.step("Pick '{option}' in 'Old Style Select Menu'")
    async def pick_old_style(self, option: str):
        await self.page.locator("#oldSelectMenu").select_option(label=option)

    async def get_old_style_value(self) -> str:
        return await self.page.locator("#oldSelectMenu").input_value()

    @allure.step("Pick standard multi-select options {options}")
    async def pick_standard_multi(self, options: list):
        await self.page.locator("select[multiple]").select_option(label=options)

    async def get_standard_multi_values(self) -> list:
        select = self.page.locator("select[multiple]")
        return await select.evaluate(
            "(el) => Array.from(el.selectedOptions).map(o => o.text)"
        )
