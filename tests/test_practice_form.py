import os
from pathlib import Path

import pytest

from pages.demoqa_practice_form_page import DemoqaPracticeFormPage
from utilities.logger import get_logger

logger = get_logger()

UPLOAD_FILE = str(Path(__file__).parent / "fixtures" / "upload_sample.txt")


@pytest.mark.regression
@pytest.mark.asyncio
async def test_practice_form_happy_path(page):
    """End-to-end submission of the Practice Form with the canonical mix of inputs."""
    form = DemoqaPracticeFormPage(page)
    await form.navigate_to_form()

    await form.fill_personal_details(
        first_name="Ada",
        last_name="Lovelace",
        email="ada@example.com",
        mobile="9876543210",
    )
    await form.select_gender("Female")
    await form.set_date_of_birth("14 May 1990")
    await form.add_subjects(["Maths", "Computer Science"])
    await form.select_hobbies(["Sports", "Reading"])
    await form.upload_picture(UPLOAD_FILE)
    await form.fill_current_address("221B Baker Street, London")
    await form.select_state_and_city("NCR", "Delhi")
    await form.submit()

    rows = await form.get_confirmation_rows()
    logger.info(f"Confirmation rows: {rows}")

    assert rows["Student Name"] == "Ada Lovelace"
    assert rows["Student Email"] == "ada@example.com"
    assert rows["Gender"] == "Female"
    assert rows["Mobile"] == "9876543210"
    assert rows["Date of Birth"] == "14 May,1990"
    assert "Maths" in rows["Subjects"] and "Computer Science" in rows["Subjects"]
    assert "Sports" in rows["Hobbies"] and "Reading" in rows["Hobbies"]
    assert rows["Picture"] == os.path.basename(UPLOAD_FILE)
    assert rows["Address"] == "221B Baker Street, London"
    assert rows["State and City"] == "NCR Delhi"

    await form.close_confirmation_modal()
