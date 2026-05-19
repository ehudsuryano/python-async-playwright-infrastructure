import pytest

from pages.demoqa_web_tables_page import DemoqaWebTablesPage, WebTableRow


ROW = WebTableRow(
    first_name="Grace",
    last_name="Hopper",
    age="40",
    email="grace.hopper@example.com",
    salary="123456",
    department="Engineering",
)


async def _flatten(rows):
    return [cell for row in rows for cell in row]


@pytest.mark.regression
@pytest.mark.asyncio
async def test_add_row(page):
    table = DemoqaWebTablesPage(page)
    await table.navigate_to_web_tables()
    await table.add_record(ROW)

    rows = await table.get_rows()
    cells = await _flatten(rows)
    assert ROW.first_name in cells
    assert ROW.last_name in cells
    assert ROW.email in cells


@pytest.mark.regression
@pytest.mark.asyncio
async def test_search_filters_rows(page):
    table = DemoqaWebTablesPage(page)
    await table.navigate_to_web_tables()
    await table.add_record(ROW)

    await table.search(ROW.last_name)
    rows = await table.get_rows()
    assert len(rows) == 1
    assert ROW.email in rows[0]

    await table.clear_search()
    assert len(await table.get_rows()) >= 1


@pytest.mark.regression
@pytest.mark.asyncio
async def test_edit_row(page):
    table = DemoqaWebTablesPage(page)
    await table.navigate_to_web_tables()
    await table.add_record(ROW)

    updated = WebTableRow(
        first_name="Grace",
        last_name="Hopper",
        age="41",
        email="grace.hopper@example.com",
        salary="999999",
        department="Research",
    )
    await table.edit_row(ROW.email, updated)

    rows = await table.get_rows()
    cells = await _flatten(rows)
    assert "999999" in cells
    assert "Research" in cells


@pytest.mark.regression
@pytest.mark.asyncio
async def test_delete_row(page):
    table = DemoqaWebTablesPage(page)
    await table.navigate_to_web_tables()
    await table.add_record(ROW)
    assert await table.find_row_index(ROW.email) is not None

    await table.delete_row(ROW.email)
    assert await table.find_row_index(ROW.email) is None
