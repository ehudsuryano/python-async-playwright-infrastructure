from typing import Iterable

import allure
from playwright.async_api import Page

from base.base_page import BasePage
from config import settings
from utilities.logger import get_logger

logger = get_logger()


class DemoqaPracticeFormPage(BasePage):
    """Page object for https://demoqa.com/automation-practice-form."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{settings.DEMOQA_BASE_URL}/automation-practice-form"

    @allure.step("Navigate to Practice Form")
    async def navigate_to_form(self):
        await self.navigate(self.url)

    @allure.step("Fill personal details")
    async def fill_personal_details(self, first_name: str, last_name: str, email: str, mobile: str):
        await self.page.locator("#firstName").fill(first_name)
        await self.page.locator("#lastName").fill(last_name)
        await self.page.locator("#userEmail").fill(email)
        await self.page.locator("#userNumber").fill(mobile)
        logger.info(f"Filled personal details for {first_name} {last_name}")

    @allure.step("Select gender '{gender}'")
    async def select_gender(self, gender: str):
        # The real <input> is hidden behind a styled label; click the label.
        await self.page.locator(f"label:has-text('{gender}')").first.click()

    @allure.step("Set date of birth to {date}")
    async def set_date_of_birth(self, date: str):
        """date in the form '14 May 1990'."""
        dob = self.page.locator("#dateOfBirthInput")
        await dob.click()
        await self.page.keyboard.press("Control+A")
        await self.page.keyboard.type(date)
        await self.page.keyboard.press("Enter")

    @allure.step("Add subjects {subjects}")
    async def add_subjects(self, subjects: Iterable[str]):
        for subject in subjects:
            box = self.page.locator("#subjectsInput")
            await box.click()
            await box.type(subject)
            # Pick the first matching suggestion.
            await self.page.locator(
                f".subjects-auto-complete__option:has-text('{subject}')"
            ).first.click()

    @allure.step("Select hobbies {hobbies}")
    async def select_hobbies(self, hobbies: Iterable[str]):
        for hobby in hobbies:
            await self.page.locator(f"label:has-text('{hobby}')").first.click()

    @allure.step("Upload picture from {file_path}")
    async def upload_picture(self, file_path: str):
        await self.page.locator("#uploadPicture").set_input_files(file_path)

    @allure.step("Fill current address")
    async def fill_current_address(self, address: str):
        await self.page.locator("#currentAddress").fill(address)

    @allure.step("Select state '{state}' and city '{city}'")
    async def select_state_and_city(self, state: str, city: str):
        await self.page.locator("#state").click()
        await self.page.get_by_text(state, exact=True).first.click()
        await self.page.locator("#city").click()
        await self.page.get_by_text(city, exact=True).first.click()

    @allure.step("Submit form")
    async def submit(self):
        # Submit can be hidden behind the demoqa.com fixed footer ad slot.
        submit = self.page.locator("#submit")
        await submit.scroll_into_view_if_needed()
        await submit.click()

    @allure.step("Read confirmation modal rows")
    async def get_confirmation_rows(self) -> dict:
        """Returns {label: value} pairs from the submission confirmation modal."""
        await self.page.locator("#example-modal-sizes-title-lg").wait_for(state="visible")
        rows = self.page.locator(".modal-body table tbody tr")
        result = {}
        for i in range(await rows.count()):
            cells = rows.nth(i).locator("td")
            label = (await cells.nth(0).text_content() or "").strip()
            value = (await cells.nth(1).text_content() or "").strip()
            result[label] = value
        return result

    @allure.step("Close confirmation modal")
    async def close_confirmation_modal(self):
        await self.page.locator("#closeLargeModal").click()
