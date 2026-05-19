from typing import Iterable

import allure
from playwright.async_api import APIResponse

from base.base_api_client import BaseApiClient
from utilities.logger import get_logger

logger = get_logger()


class BookStoreService(BaseApiClient):
    """Wraps demoqa /BookStore/v1 endpoints."""

    @allure.step("API: list books")
    async def list_books(self) -> list[dict]:
        response = await self.get("/BookStore/v1/Books")
        assert response.ok, f"List books failed: {response.status}"
        payload = await self.parse_json(response)
        return payload.get("books", [])

    @allure.step("API: get book {isbn}")
    async def get_book(self, isbn: str) -> dict:
        response = await self.get("/BookStore/v1/Book", params={"ISBN": isbn})
        assert response.ok, f"Get book failed: {response.status}"
        return await self.parse_json(response)

    @allure.step("API: add books to user {user_id}")
    async def add_books_to_user(
        self, user_id: str, token: str, isbns: Iterable[str]
    ) -> dict:
        body = {
            "userId": user_id,
            "collectionOfIsbns": [{"isbn": isbn} for isbn in isbns],
        }
        response = await self.post("/BookStore/v1/Books", json=body, token=token)
        assert response.status == 201, f"Add books failed: {response.status}"
        return await self.parse_json(response)

    @allure.step("API: delete all books for user {user_id}")
    async def delete_all_books_for_user(self, user_id: str, token: str) -> APIResponse:
        response = await self.delete(
            "/BookStore/v1/Books", params={"UserId": user_id}, token=token
        )
        assert response.status in (200, 204), f"Delete books failed: {response.status}"
        return response
