"""
Demonstration of API testing on top of the same async Playwright stack
used for the UI tests. Uses Playwright's APIRequestContext, exposed via
the `api_request_context` fixture in conftest.py.

Targets the demoqa BookStore API: https://demoqa.com/swagger/
"""
import uuid

import pytest
import pytest_asyncio

from api.account_service import AccountService
from api.book_store_service import BookStoreService
from utilities.logger import get_logger

logger = get_logger()


def _unique_username() -> str:
    return f"qa_{uuid.uuid4().hex[:10]}"


# demoqa's password policy requires upper, lower, digit, special, 8+ chars
TEST_PASSWORD = "Qa!Demo123"


@pytest_asyncio.fixture
async def account_service(api_request_context) -> AccountService:
    return AccountService(api_request_context)


@pytest_asyncio.fixture
async def book_store_service(api_request_context) -> BookStoreService:
    return BookStoreService(api_request_context)


@pytest_asyncio.fixture
async def authorized_user(account_service: AccountService):
    """Creates a fresh user, generates a token, and cleans up after the test."""
    username = _unique_username()
    created = await account_service.create_user(username, TEST_PASSWORD)
    user_id = created["userID"]
    token_payload = await account_service.generate_token(username, TEST_PASSWORD)
    token = token_payload["token"]

    yield {"user_id": user_id, "username": username, "token": token}

    try:
        await account_service.delete_user(user_id, token)
    except AssertionError as e:
        logger.warning(f"User cleanup failed for {user_id}: {e}")


@pytest.mark.asyncio
async def test_list_books_returns_catalog(book_store_service: BookStoreService):
    """GET /BookStore/v1/Books returns a non-empty catalog."""
    books = await book_store_service.list_books()
    assert isinstance(books, list)
    assert len(books) > 0
    assert all("isbn" in book and "title" in book for book in books)


@pytest.mark.asyncio
async def test_get_single_book_by_isbn(book_store_service: BookStoreService):
    """GET /BookStore/v1/Book?ISBN=... returns a single matching record."""
    books = await book_store_service.list_books()
    sample_isbn = books[0]["isbn"]
    book = await book_store_service.get_book(sample_isbn)
    assert book["isbn"] == sample_isbn
    assert book["title"]


@pytest.mark.asyncio
async def test_get_book_with_invalid_isbn_returns_400(
    book_store_service: BookStoreService,
):
    """Negative-path: bad ISBN returns 4xx."""
    response = await book_store_service.get("/BookStore/v1/Book", params={"ISBN": "not-real"})
    assert response.status == 400


@pytest.mark.asyncio
async def test_create_user_and_authorize(account_service: AccountService):
    """End-to-end auth flow against /Account/v1."""
    username = _unique_username()
    created = await account_service.create_user(username, TEST_PASSWORD)
    assert created["username"] == username
    assert created["books"] == []

    token_payload = await account_service.generate_token(username, TEST_PASSWORD)
    assert token_payload["status"] == "Success"
    assert token_payload["token"]

    is_authorized = await account_service.is_authorized(username, TEST_PASSWORD)
    assert is_authorized is True

    await account_service.delete_user(created["userID"], token_payload["token"])


@pytest.mark.asyncio
async def test_add_book_to_user_collection(
    authorized_user, account_service: AccountService, book_store_service: BookStoreService
):
    """Full flow: pick a book, add it to a user, verify it appears, clean up."""
    books = await book_store_service.list_books()
    target_isbn = books[0]["isbn"]

    await book_store_service.add_books_to_user(
        authorized_user["user_id"], authorized_user["token"], [target_isbn]
    )

    user = await account_service.get_user(authorized_user["user_id"], authorized_user["token"])
    user_isbns = [book["isbn"] for book in user["books"]]
    assert target_isbn in user_isbns

    await book_store_service.delete_all_books_for_user(
        authorized_user["user_id"], authorized_user["token"]
    )
    user = await account_service.get_user(authorized_user["user_id"], authorized_user["token"])
    assert user["books"] == []
