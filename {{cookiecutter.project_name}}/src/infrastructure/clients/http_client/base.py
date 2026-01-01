from json import JSONDecodeError
import typing as t

import httpx
from httpx import Response

from src.infrastructure.clients.http_client.client import HttpClient
from src.infrastructure.core.errors.exceptions import ExternalServiceError


def handle_response_middleware(service_name: str) -> t.Callable:
    async def check_response(data: dict, handler: t.Callable) -> Response:
        """
        Middleware to check the response of the remote infrastructure. If the response is negative, an error is generated
        """

        response: httpx.Response = await handler(data)

        if response.status_code not in (200, 201, 204):
            try:
                details: dict[str, t.Any] = response.json()
            except JSONDecodeError:
                details: str = response.text or None
            raise ExternalServiceError(
                message=f"Unsuccessful interaction with {service_name}: {details}", code=response.status_code
            )

        return response

    return check_response


class BaseClient:
    def _init_api(self, client: HttpClient) -> t.Never:
        raise NotImplementedError

    def __init__(self, url: str, headers: dict[str, t.Any] = None, **kwargs: dict) -> None:
        self._client: HttpClient = HttpClient(base_url=url, headers=headers, **kwargs)
        self._init_api(self._client)

    async def __aenter__(self) -> "BaseClient":
        return self

    async def __aexit__(self, exc_type: str, exc_val: str, exc_tb: str) -> None:
        await self._client.close()

    async def close(self) -> None:
        await self._client.close()
