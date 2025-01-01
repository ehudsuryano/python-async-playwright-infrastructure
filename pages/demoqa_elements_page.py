from pyexpat.errors import messages
from exceptions.exceptions import ElementNotFoundException, WebElementException
from handlers.textbox_handler import TextboxHandler
from handlers.demohqSideMenuItem_Handler import SideMenuItemHandler
from handlers.button_handler import ButtonHandler
from utilities.logger import get_logger
from base.base_page import BasePage  # Import the BasePage class
from playwright.async_api import Error as PlaywrightError
from playwright.async_api import TimeoutError
logger = get_logger()


class DemoqaElementsPage(BasePage):  # Inherit from BasePage
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://demoqa.com/elements"

    async def navigate_to_elements(self):
        await self.navigate(self.url)

    async def click_side_menu_item(self, page, item_name):
        try:
            await page.get_by_text(item_name).click()
            logger.info(f"side menu item{item_name}  was clicked")
        except TimeoutError:
            logger.error(f"side menu item{item_name} was NOT clicked -> {TimeoutError}")
        return

    async def type_text(self, page, text_box_placeholder=None, text_box_id=None, text=""):
        try:
            if text_box_placeholder:
                element = page.get_by_placeholder(text_box_placeholder)
            elif text_box_id:
                element = page.locator(f"#{text_box_id}")
            else:
                logger.error("Neither placeholder nor id was provided to locate the text box.")
                return

            await element.type(text)
            logger.info(f'"{text}" was typed into the element identified by '
                        f'{"placeholder: " + text_box_placeholder if text_box_placeholder else "id: " + text_box_id}')
        except TimeoutError:
            logger.error(f'"{text}" was NOT typed into the element identified by '
                         f'{"placeholder: " + text_box_placeholder if text_box_placeholder else "id: " + text_box_id}')

    async def click_button(self, page, btn_name):
        try:
            await page.get_by_role("button", name=btn_name).click()
            logger.info(f"side menu item{btn_name}  was clicked")
        except TimeoutError:
            logger.error(f"side menu item{btn_name} was NOT clicked")
        return

    async def type_text_by_handler(self, page, text_element, text_to_type):
        try:
            elements = await TextboxHandler.get_elements(page, text_element)
            if elements:  # Add a check to make sure we found elements
                await elements[0].fill(text_to_type)  # Using fill() instead of type() for better reliability
            logger.info(f'"{text_to_type}" was typed into the element identified by {text_element}')
        except TimeoutError:
            logger.error(f'"{text_to_type}" was NOT typed into the element identified by {text_element}')

    async def click_side_menu_item_by_handler(self, page, item_name):
        try:
            elements = await SideMenuItemHandler.get_elements(page, item_name)
            if elements:  # Add a check to make sure we found elements
                await elements[0].click() # Click the first element found
            logger.info(f"side menu item{item_name}  was clicked")
        except TimeoutError:
            logger.error(f"side menu item{item_name} was NOT clicked -> {TimeoutError}")
        return

    async def click_button_by_handler(self, page, btn_name):
        try:
            elements = await ButtonHandler.get_elements(page, btn_name)
            if elements:  # Add a check to make sure we found elements
                await elements[0].click()  # Click the first element found
            logger.info(f"side menu item{btn_name}  was clicked")
        except TimeoutError:
            logger.error(f"side menu item{btn_name} was NOT clicked")
        return