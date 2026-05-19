from dataclasses import dataclass
from typing import List, Optional

import allure
from playwright.async_api import Page

from base.base_page import BasePage
from config import settings
from utilities.logger import get_logger

logger = get_logger()


@dataclass
class WebTableRow:
    first_name: str
    last_name: str
    age: str
    email: str
    salary: str
    department: str


class DemoqaWebTablesPage(BasePage):
    """Page object for https://demoqa.com/webtables."""

    ROW_SELECTOR = "table tbody tr"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{settings.DEMOQA_BASE_URL}/webtables"

    @allure.step("Navigate to Web Tables")
    async def navigate_to_web_tables(self):
        await self.navigate(self.url)

    async def _fill_row_form(self, row: WebTableRow):
        await self.page.locator("#firstName").fill(row.first_name)
        await self.page.locator("#lastName").fill(row.last_name)
        await self.page.locator("#userEmail").fill(row.email)
        await self.page.locator("#age").fill(row.age)
        await self.page.locator("#salary").fill(row.salary)
        await self.page.locator("#department").fill(row.department)
        await self.page.locator("#submit").click()
        await self.page.locator(".modal").wait_for(state="hidden")

    @allure.step("Add new record")
    async def add_record(self, row: WebTableRow):
        await self.page.locator("#addNewRecordButton").click()
        await self._fill_row_form(row)

    @allure.step("Search '{query}'")
    async def search(self, query: str):
        await self.page.locator("#searchBox").fill(query)

    @allure.step("Clear search")
    async def clear_search(self):
        await self.page.locator("#searchBox").fill("")

    async def get_rows(self) -> List[List[str]]:
        rows = self.page.locator(self.ROW_SELECTOR)
        result = []
        for i in range(await rows.count()):
            cells = rows.nth(i).locator("td")
            values = [(await cells.nth(j).text_content() or "").strip() for j in range(await cells.count())]
            result.append(values)
        return result

    async def find_row_index(self, email: str) -> Optional[int]:
        rows = await self.get_rows()
        for idx, cells in enumerate(rows):
            if email in cells:
                return idx
        return None

    @allure.step("Edit row with email {email}")
    async def edit_row(self, email: str, updated: WebTableRow):
        idx = await self.find_row_index(email)
        assert idx is not None, f"No row found with email {email}"
        row = self.page.locator(self.ROW_SELECTOR).nth(idx)
        await row.locator("[title='Edit']").click()
        await self._fill_row_form(updated)

    @allure.step("Delete row with email {email}")
    async def delete_row(self, email: str):
        idx = await self.find_row_index(email)
        assert idx is not None, f"No row found with email {email}"
        row = self.page.locator(self.ROW_SELECTOR).nth(idx)
        await row.locator("[title='Delete']").click()
