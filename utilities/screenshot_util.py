import allure
import os
from datetime import datetime
from playwright.async_api import Page
from config import settings


async def capture_screenshot(page: Page, name: str):
    """
    Captures a screenshot of the current browser state and attaches it to the Allure report.

    Args:
        page (Page): The Playwright Page instance.
        name (str): Name for the screenshot file (without extension).
    """
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Set the full path for the screenshot
    screenshot_path = os.path.join(settings.REPORT_PATH, f"{name}_{now}.png")

    # Save the screenshot locally
    await page.screenshot(path=screenshot_path)

    # Attach the screenshot to the Allure report
    with open(screenshot_path, "rb") as image_file:
        allure.attach(
            image_file.read(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
