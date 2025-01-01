from base.base_page import BasePage
import allure
from utilities.logger import get_logger
from exceptions.exceptions import ElementNotFoundException, WebElementException
from handlers.card_handler import CardHandler


logger = get_logger()

class DemoqaHomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://demoqa.com/"

    @allure.step("Navigate to home page")
    async def navigate_to_home(self):
        await self.navigate(self.url)

    @allure.step("Get page title")
    async def verify_title_contains(self, expected_text: str) -> bool:
        title = await self.get_title()
        return expected_text in title

    @allure.step("click on Elements card")
    async def click_elements(self, page):
        try:
            await page.get_by_text("Elements").click()
            logger.info("Elements card was clicked")
        except Exception("element not found") as e:
            logger.error(f"Elements card was NOT clicked {e}")
        return

    @allure.step("click on Widgets card")
    async def click_widgets(self, page):
        try:
            await page.get_by_text("Widgets").click()
            logger.info("Widgets card was clicked")
        except Exception as e:
            logger.error("Widgets card was NOT clicked")
        return

    async def click_card(self, page, card_name: str):
        try:
            elements = await CardHandler.get_elements(page, card_name)
            if elements:  # Add a check to make sure we found elements
                await elements[0].click() # Click the first element found
            logger.info(f"Card with name '{card_name}' was clicked")
        except Exception as e:
            logger.error(f"Card with name '{card_name}' was NOT clicked")
        return