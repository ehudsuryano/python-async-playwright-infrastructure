# Contents of conftest.py file
import os
import asyncio
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from datetime import datetime
from config import settings
from utilities.screenshot_util import capture_screenshot


@pytest_asyncio.fixture(scope="function")
async def playwright():
    """Initialize Playwright session."""
    async with async_playwright() as pw:
        yield pw

@pytest_asyncio.fixture(scope="function")
async def browser(playwright):
    """Launch the browser instance."""
    browser = await playwright.chromium.launch(headless=False)
    yield browser
    await browser.close()

@pytest_asyncio.fixture(scope="function")
async def page(browser):
    """Create a new browser context and page for each test."""
    context = await browser.new_context()
    page = await context.new_page()
    await page.context.tracing.start(screenshots=True, snapshots=True)
    yield page
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    trace_path = f"{settings.TRACE_PATH}/trace_{now}.zip"
    await page.context.tracing.stop(path=trace_path)
    await context.close()


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = f"{settings.REPORT_PATH}/report_{now}.html"


