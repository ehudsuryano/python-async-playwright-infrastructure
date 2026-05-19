from typing import Optional

import allure
from playwright.async_api import Dialog, Page

from base.base_page import BasePage
from config import settings


class DemoqaAlertsPage(BasePage):
    """Page object for https://demoqa.com/alerts."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{settings.DEMOQA_BASE_URL}/alerts"
        self.last_dialog_message: Optional[str] = None

    @allure.step("Navigate to Alerts page")
    async def navigate_to_alerts(self):
        await self.navigate(self.url)

    def _capture_dialog(self, accept: bool = True, prompt_text: Optional[str] = None):
        """Register a one-shot dialog handler and record the message it carried."""
        self.last_dialog_message = None

        async def handler(dialog: Dialog):
            self.last_dialog_message = dialog.message
            if accept:
                await dialog.accept(prompt_text) if prompt_text is not None else await dialog.accept()
            else:
                await dialog.dismiss()

        self.page.once("dialog", handler)

    @allure.step("Trigger simple alert")
    async def trigger_simple_alert(self):
        self._capture_dialog(accept=True)
        await self.page.locator("#alertButton").click()

    @allure.step("Trigger confirm dialog (accept={accept})")
    async def trigger_confirm(self, accept: bool):
        self._capture_dialog(accept=accept)
        await self.page.locator("#confirmButton").click()

    @allure.step("Trigger prompt with text '{text}'")
    async def trigger_prompt(self, text: str):
        self._capture_dialog(accept=True, prompt_text=text)
        await self.page.locator("#promtButton").click()

    async def confirm_result_text(self) -> str:
        return (await self.page.locator("#confirmResult").text_content()) or ""

    async def prompt_result_text(self) -> str:
        return (await self.page.locator("#promptResult").text_content()) or ""
