# test_demoqa.py
import time
from asyncio import timeout

import pytest
import os
from datetime import datetime
from pages.demoqa_home_page import DemoqaHomePage
from pages.demoqa_elements_page import DemoqaElementsPage
from utilities.logger import get_logger
from config import settings
from utilities.screenshot_util import capture_screenshot

logger = get_logger()

@pytest.mark.asyncio
async def test_has_title_demoqa(page):
    """Validate DEMOQA Main page title"""
    await page.goto("https://demoqa.com/")
    title = await page.title()
    assert title == "DEMOQA"

@pytest.mark.asyncio
async def test_has_title_POM_demoqa(page):
    """Validate DEMOQA Main page title"""
    logger.info("Starting test for Home Page")
    demoqa_home_page = DemoqaHomePage(page)
    await demoqa_home_page.navigate_to_home()
    title = await page.title()
    logger.info("Loaded Home Page")
    try:
        assert title == "DEMOQA"
        logger.info("Test passed")
    except AssertionError as e:
        # Capture a screenshot on failure
        logger.error(f"Test failed, screenshot captured at check {settings.REPORT_PATH}")
        raise

@pytest.mark.asyncio
async def test_reach_elements_page(page):
    logger.info("Starting test for Elements Page")
    home_page = DemoqaHomePage(page)
    await home_page.navigate_to_home()
    logger.info("Loaded Home Page")
    await home_page.click_elements(page)
    logger.info("Loaded Elements Page")
    elements_page = DemoqaElementsPage(page)
    await elements_page.click_side_menu_item(page, "Text Box")
    await elements_page.click_side_menu_item(page, "Check Box")
    await elements_page.click_side_menu_item(page, "Radio Button")
    await elements_page.click_side_menu_item(page, "Web Tables")
    logger.info("All elements clicked")
    await elements_page.click_side_menu_item(page, "Text Box")
    await elements_page.type_text(page, "Full Name", text="John Doe")
    await elements_page.type_text(page, "name@example.com", text="Johnoe@gmail.com")
    await elements_page.type_text(page, "Current Address", text="123 Main St")
    await elements_page.type_text(page, text_box_id="permanentAddress", text="456 Elm St")
    logger.info("All text boxes filled")
    await elements_page.click_button(page, "Submit")
    logger.info("Submit button clicked")
    time.sleep(5)
    try:
        assert "https://demoqa.com/text-box" in await elements_page.get_url(), "Page title mismatch"
        logger.info("Test passed")
        assert await elements_page.is_element_exist("#output") is True, "can't find output"
        logger.info("output exists")
    except AssertionError as e:
        # Capture screenshot on failure
        await capture_screenshot(page, "failure-home-page")
        logger.error("Test failed, screenshot captured")
        raise

@pytest.mark.asyncio
async def test_has_title_google(page):
    """Validate Google Main page title"""
    await page.goto("https://www.google.com/")
    title = await page.title()
    assert title == "Googleeee"

@pytest.mark.asyncio
async def test_has_title_playwright(page):
    """Validate Google Main page title"""
    await page.goto("https://playwright.dev/python")
    title = await page.title()
    assert "Playwright" in title, "Page title mismatch"

@pytest.mark.asyncio
async def test_reach_elements_page2(page):
    logger.info("Starting test for Elements Page")
    home_page = DemoqaHomePage(page)
    await home_page.navigate_to_home()
    logger.info("Loaded Home Page")
    await home_page.click_card(page, "Elements")
    logger.info("Loaded Elements Page")
    elements_page = DemoqaElementsPage(page)
    await elements_page.click_side_menu_item_by_handler(page, "Text Box")
    await elements_page.type_text_by_handler(page, "Full Name", "John Doe")
    await elements_page.type_text_by_handler(page, "name@example.com", "Johnoe@gmail.com")
    await elements_page.type_text_by_handler(page, "Current Address", "123 Main St")
    await elements_page.type_text_by_handler(page, "permanentAddress", "456 Elm St")
    logger.info("All text boxes filled")
    await elements_page.click_button_by_handler(page, "Submit")
    logger.info("Submit button clicked")