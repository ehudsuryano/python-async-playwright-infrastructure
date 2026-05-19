import allure
from playwright.async_api import Page

from base.base_page import BasePage
from config import settings


class DemoqaFramesPage(BasePage):
    """Page object for https://demoqa.com/frames and /nestedframes."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.frames_url = f"{settings.DEMOQA_BASE_URL}/frames"
        self.nested_frames_url = f"{settings.DEMOQA_BASE_URL}/nestedframes"

    @allure.step("Navigate to Frames page")
    async def navigate_to_frames(self):
        await self.navigate(self.frames_url)

    @allure.step("Navigate to Nested Frames page")
    async def navigate_to_nested_frames(self):
        await self.navigate(self.nested_frames_url)

    async def get_frame_heading_text(self, frame_id: str) -> str:
        frame = self.page.frame_locator(f"#{frame_id}")
        return (await frame.locator("#sampleHeading").text_content()) or ""

    async def get_nested_parent_text(self) -> str:
        return (await self.page.frame_locator("#frame1").locator("body").text_content()) or ""

    async def get_nested_child_text(self) -> str:
        parent = self.page.frame_locator("#frame1")
        child = parent.frame_locator("iframe")
        return (await child.locator("p").text_content()) or ""
