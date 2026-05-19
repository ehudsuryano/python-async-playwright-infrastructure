import pytest

from pages.demoqa_date_picker_page import DemoqaDatePickerPage
from pages.demoqa_progress_bar_page import DemoqaProgressBarPage
from pages.demoqa_select_menu_page import DemoqaSelectMenuPage
from pages.demoqa_slider_page import DemoqaSliderPage
from pages.demoqa_tabs_page import DemoqaTabsPage
from pages.demoqa_tooltips_page import DemoqaTooltipsPage


@pytest.mark.regression
@pytest.mark.asyncio
async def test_date_picker_sets_date(page):
    dp = DemoqaDatePickerPage(page)
    await dp.navigate_to_date_picker()
    await dp.set_date("07/04/2026")
    assert await dp.get_date() == "07/04/2026"


@pytest.mark.regression
@pytest.mark.asyncio
async def test_select_menu_old_style(page):
    sm = DemoqaSelectMenuPage(page)
    await sm.navigate_to_select_menu()
    await sm.pick_old_style("Blue")
    assert await sm.get_old_style_value() == "1"  # value attr for "Blue"


@pytest.mark.regression
@pytest.mark.asyncio
async def test_select_menu_react_select_value(page):
    sm = DemoqaSelectMenuPage(page)
    await sm.navigate_to_select_menu()
    await sm.pick_select_value("Group 1, option 2")
    assert "Group 1, option 2" in await sm.get_selected_value()


@pytest.mark.regression
@pytest.mark.asyncio
async def test_select_menu_standard_multi(page):
    sm = DemoqaSelectMenuPage(page)
    await sm.navigate_to_select_menu()
    await sm.pick_standard_multi(["Volvo", "Audi"])
    selected = await sm.get_standard_multi_values()
    assert "Volvo" in selected and "Audi" in selected


@pytest.mark.regression
@pytest.mark.asyncio
async def test_slider_moves_to_target(page):
    slider = DemoqaSliderPage(page)
    await slider.navigate_to_slider()
    await slider.move_slider_to(50)
    assert await slider.get_value() == "50"


@pytest.mark.regression
@pytest.mark.asyncio
async def test_progress_bar_reaches_100(page):
    bar = DemoqaProgressBarPage(page)
    await bar.navigate_to_progress_bar()
    await bar.start()
    await bar.wait_for_complete()
    assert await bar.get_value() == "100"


@pytest.mark.regression
@pytest.mark.asyncio
async def test_tabs_switching(page):
    tabs = DemoqaTabsPage(page)
    await tabs.navigate_to_tabs()

    await tabs.open_tab("what")
    assert "Lorem Ipsum" in await tabs.panel_text("what")

    await tabs.open_tab("origin")
    assert "Lorem Ipsum" in await tabs.panel_text("origin")

    await tabs.open_tab("use")
    assert "Lorem Ipsum" in await tabs.panel_text("use")


@pytest.mark.regression
@pytest.mark.asyncio
async def test_tooltip_on_button(page):
    tooltips = DemoqaTooltipsPage(page)
    await tooltips.navigate_to_tooltips()
    text = await tooltips.hover_button_tooltip()
    assert "You hovered over the Button" in text
