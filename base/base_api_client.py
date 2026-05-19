from typing import Any, Mapping, Optional

from playwright.async_api import APIRequestContext, APIResponse

from utilities.logger import get_logger

logger = get_logger()


class BaseApiClient:
    def __init__(self, request_context: APIRequestContext, base_url: str = ""):
        self.request = request_context
        self.base_url = base_url.rstrip("/")

    def _url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        if not self.base_url:
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    @staticmethod
    def _auth_headers(token: Optional[str]) -> dict:
        return {"Authorization": f"Bearer {token}"} if token else {}

    async def _log_response(self, method: str, url: str, response: APIResponse) -> None:
        logger.info(f"{method} {url} -> {response.status}")
        if not response.ok:
            body = await response.text()
            logger.error(f"Non-OK response body: {body[:500]}")

    async def get(
        self,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        token: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> APIResponse:
        url = self._url(path)
        merged_headers = {**self._auth_headers(token), **(headers or {})}
        response = await self.request.get(url, params=params, headers=merged_headers)
        await self._log_response("GET", url, response)
        return response

    async def post(
        self,
        path: str,
        *,
        json: Optional[Any] = None,
        token: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> APIResponse:
        url = self._url(path)
        merged_headers = {**self._auth_headers(token), **(headers or {})}
        response = await self.request.post(url, data=json, headers=merged_headers)
        await self._log_response("POST", url, response)
        return response

    async def delete(
        self,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        token: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> APIResponse:
        url = self._url(path)
        merged_headers = {**self._auth_headers(token), **(headers or {})}
        response = await self.request.delete(url, params=params, headers=merged_headers)
        await self._log_response("DELETE", url, response)
        return response

    @staticmethod
    async def parse_json(response: APIResponse) -> Any:
        return await response.json()
