# Contents of conftest.py file
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from datetime import datetime
from config import settings
from utilities.screenshot_util import capture_screenshot


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Expose each phase's outcome on the test item so fixtures can react to it."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


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
async def page(browser, request):
    """Create a new browser context and page for each test."""
    context = await browser.new_context()
    page = await context.new_page()
    await page.context.tracing.start(screenshots=True, snapshots=True)
    yield page

    failed = (
        (getattr(request.node, "rep_setup", None) and request.node.rep_setup.failed)
        or (getattr(request.node, "rep_call", None) and request.node.rep_call.failed)
    )
    if failed:
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_name = request.node.name.replace("/", "_").replace(":", "_")
        trace_path = f"{settings.TRACE_PATH}/trace_{safe_name}_{now}.zip"
        await page.context.tracing.stop(path=trace_path)
    else:
        await page.context.tracing.stop()
    await context.close()


@pytest_asyncio.fixture(scope="function")
async def api_request_context(playwright):
    """APIRequestContext for backend testing — independent of any browser."""
    context = await playwright.request.new_context(
        base_url=settings.DEMOQA_API_BASE_URL,
        extra_http_headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        timeout=settings.API_DEFAULT_TIMEOUT_MS,
    )
    yield context
    await context.dispose()


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = f"{settings.REPORT_PATH}/report_{now}.html"
