import pytest

from pages.demoqa_alerts_page import DemoqaAlertsPage
from pages.demoqa_browser_windows_page import DemoqaBrowserWindowsPage
from pages.demoqa_frames_page import DemoqaFramesPage
from pages.demoqa_modal_dialogs_page import DemoqaModalDialogsPage


@pytest.mark.regression
@pytest.mark.asyncio
async def test_simple_alert_is_handled(page):
    alerts = DemoqaAlertsPage(page)
    await alerts.navigate_to_alerts()
    await alerts.trigger_simple_alert()
    assert alerts.last_dialog_message == "You clicked a button"


@pytest.mark.regression
@pytest.mark.asyncio
async def test_confirm_accept_shows_ok(page):
    alerts = DemoqaAlertsPage(page)
    await alerts.navigate_to_alerts()
    await alerts.trigger_confirm(accept=True)
    assert "You selected Ok" in await alerts.confirm_result_text()


@pytest.mark.regression
@pytest.mark.asyncio
async def test_confirm_dismiss_shows_cancel(page):
    alerts = DemoqaAlertsPage(page)
    await alerts.navigate_to_alerts()
    await alerts.trigger_confirm(accept=False)
    assert "You selected Cancel" in await alerts.confirm_result_text()


@pytest.mark.regression
@pytest.mark.asyncio
async def test_prompt_echoes_typed_text(page):
    alerts = DemoqaAlertsPage(page)
    await alerts.navigate_to_alerts()
    await alerts.trigger_prompt("Alan Turing")
    assert "Alan Turing" in await alerts.prompt_result_text()


@pytest.mark.regression
@pytest.mark.asyncio
async def test_single_frame_heading(page):
    frames = DemoqaFramesPage(page)
    await frames.navigate_to_frames()
    assert await frames.get_frame_heading_text("frame1") == "This is a sample page"


@pytest.mark.regression
@pytest.mark.asyncio
async def test_nested_frame_child_text(page):
    frames = DemoqaFramesPage(page)
    await frames.navigate_to_nested_frames()
    assert "Parent frame" in await frames.get_nested_parent_text()
    assert "Child Iframe" in await frames.get_nested_child_text()


@pytest.mark.regression
@pytest.mark.asyncio
async def test_browser_windows_open_new_tab(page):
    windows = DemoqaBrowserWindowsPage(page)
    await windows.navigate_to_browser_windows()
    new_tab = await windows.open_new_tab()
    try:
        assert "sample" in new_tab.url
        assert (await new_tab.locator("#sampleHeading").text_content()) == "This is a sample page"
    finally:
        await new_tab.close()


@pytest.mark.regression
@pytest.mark.asyncio
async def test_browser_windows_open_new_window(page):
    windows = DemoqaBrowserWindowsPage(page)
    await windows.navigate_to_browser_windows()
    new_win = await windows.open_new_window()
    try:
        assert (await new_win.locator("#sampleHeading").text_content()) == "This is a sample page"
    finally:
        await new_win.close()


@pytest.mark.regression
@pytest.mark.asyncio
async def test_small_modal_opens_and_closes(page):
    modals = DemoqaModalDialogsPage(page)
    await modals.navigate_to_modal_dialogs()
    await modals.open_small_modal()
    assert "small modal" in (await modals.small_modal_body_text()).lower()
    await modals.close_small_modal()


@pytest.mark.regression
@pytest.mark.asyncio
async def test_large_modal_opens_and_closes(page):
    modals = DemoqaModalDialogsPage(page)
    await modals.navigate_to_modal_dialogs()
    await modals.open_large_modal()
    body = await modals.large_modal_body_text()
    assert "Lorem Ipsum" in body
    await modals.close_large_modal()
