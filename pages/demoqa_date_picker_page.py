import allure
from playwright.async_api import Page

from base.base_page import BasePage
from config import settings


class DemoqaDatePickerPage(BasePage):
    """Page object for https://demoqa.com/date-picker."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{settings.DEMOQA_BASE_URL}/date-picker"

    @allure.step("Navigate to Date Picker page")
    async def navigate_to_date_picker(self):
        await self.navigate(self.url)

    @allure.step("Set date to {date}")
    async def set_date(self, date: str):
        """date in MM/DD/YYYY format."""
        field = self.page.locator("#datePickerMonthYearInput")
        await field.click()
        await field.press("Control+A")
        await field.type(date)
        await field.press("Enter")

    async def get_date(self) -> str:
        return await self.page.locator("#datePickerMonthYearInput").input_value()

    @allure.step("Set date and time to {value}")
    async def set_date_and_time(self, value: str):
        field = self.page.locator("#dateAndTimePickerInput")
        await field.click()
        await field.press("Control+A")
        await field.type(value)
        await field.press("Enter")

    async def get_date_and_time(self) -> str:
        return await self.page.locator("#dateAndTimePickerInput").input_value()
