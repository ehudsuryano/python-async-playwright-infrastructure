import allure
from playwright.async_api import Page

from base.base_page import BasePage
from config import settings


class DemoqaSliderPage(BasePage):
    """Page object for https://demoqa.com/slider."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{settings.DEMOQA_BASE_URL}/slider"

    @allure.step("Navigate to Slider page")
    async def navigate_to_slider(self):
        await self.navigate(self.url)

    @allure.step("Move slider to {target}")
    async def move_slider_to(self, target: int):
        """Use keyboard arrows for deterministic positioning (avoids mouse drag flakiness)."""
        slider = self.page.locator(".range-slider")
        await slider.focus()
        current = int(await self.get_value())
        diff = target - current
        key = "ArrowRight" if diff > 0 else "ArrowLeft"
        for _ in range(abs(diff)):
            await slider.press(key)

    async def get_value(self) -> str:
        return await self.page.locator("#sliderValue").input_value()
