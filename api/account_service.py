from typing import Any

import allure
from playwright.async_api import APIResponse

from base.base_api_client import BaseApiClient
from utilities.logger import get_logger

logger = get_logger()


class AccountService(BaseApiClient):
    """Wraps demoqa /Account/v1 endpoints."""

    @allure.step("API: create user '{username}'")
    async def create_user(self, username: str, password: str) -> dict:
        response = await self.post(
            "/Account/v1/User",
            json={"userName": username, "password": password},
        )
        assert response.status == 201, f"Create user failed: {response.status}"
        return await self.parse_json(response)

    @allure.step("API: generate token for '{username}'")
    async def generate_token(self, username: str, password: str) -> dict:
        response = await self.post(
            "/Account/v1/GenerateToken",
            json={"userName": username, "password": password},
        )
        assert response.ok, f"Generate token failed: {response.status}"
        return await self.parse_json(response)

    @allure.step("API: check authorized for '{username}'")
    async def is_authorized(self, username: str, password: str) -> bool:
        response = await self.post(
            "/Account/v1/Authorized",
            json={"userName": username, "password": password},
        )
        assert response.ok, f"Authorized check failed: {response.status}"
        return await self.parse_json(response)

    @allure.step("API: get user {user_id}")
    async def get_user(self, user_id: str, token: str) -> dict:
        response = await self.get(f"/Account/v1/User/{user_id}", token=token)
        assert response.ok, f"Get user failed: {response.status}"
        return await self.parse_json(response)

    @allure.step("API: delete user {user_id}")
    async def delete_user(self, user_id: str, token: str) -> APIResponse:
        response = await self.delete(f"/Account/v1/User/{user_id}", token=token)
        assert response.status in (200, 204), f"Delete user failed: {response.status}"
        return response
