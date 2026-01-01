from enum import StrEnum
import typing as t
from functools import wraps

from src.infrastructure.clients.http_client.base import BaseClient, handle_response_middleware
from src.infrastructure.clients.http_client.client import HttpClient, ApiCall
from src.infrastructure.core.settings import AppConfig


class ContentType(StrEnum):
    FORM = "application/x-www-form-urlencoded"
    JSON = "application/json"


class IDPService(BaseClient):
    def __init__(self, url: str, secret: str, client_name: str, *args: str, **kwargs: str) -> None:
        self.secret = secret
        self.client_name = client_name.lower()
        self.access_token = None
        super().__init__(url, *args, **kwargs)

    def _init_api(self, client: HttpClient) -> None:
        middleware: t.Callable = handle_response_middleware("IDPService")

        self._sign_in: ApiCall = ApiCall(
            client=client, path="/openid-connect/token", method="POST", middleware=[middleware]
        )

        self._get_userinfo: ApiCall = ApiCall(
            client=client, path="/openid-connect/userinfo", method="GET", middleware=[middleware]
        )

        self._sign_out: ApiCall = ApiCall(
            client=client, path="/openid-connect/logout", method="POST", middleware=[middleware]
        )

    @staticmethod
    def check_access_token(func: t.Callable) -> t.Callable:
        @wraps(func)
        async def wrapped(instance: "IDPService", *args: str) -> t.Any:  # noqa ANN401
            if not instance.access_token:
                instance.access_token = await instance.get_service_access_token()
            return await func(instance, *args)

        return wrapped

    async def get_service_access_token(self) -> str:
        """Get infrastructure access token"""
        result = await self._sign_in(
            headers={"Content-Type": ContentType.FORM.value},
            data={
                "client_id": self.client_name,
                "grant_type": "client_credentials",
                "client_secret": self.secret,
                "scope": "openid roles",
            },
        )
        self.access_token: str = result.json()["access_token"]
        return self.access_token

    async def sign_in(self, data: dict[str, t.Any], user_ip: str) -> dict[str, t.Any]:
        """Get user access token"""
        result = await self._sign_in(
            headers={"Content-Type": ContentType.FORM.value, "X-Forwarded-For": user_ip}, data=data
        )
        return result.json()

    async def get_user_info(self, user_access_token: str) -> dict[str, t.Any] | None:
        """Get user info by access token"""
        response = await self._get_userinfo(headers={"Authorization": f"Bearer {user_access_token}"})
        return response.json() if response.status_code == 200 else None

    async def sign_out(self, access_token: str, data: dict) -> dict[str, t.Any]:
        """Sign out"""
        return await self._sign_out(
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": ContentType.FORM.value}, data=data
        )

    @staticmethod
    def new(config: AppConfig) -> "IDPService":
        return IDPService(config.IDP_URL, config.IDP_CLIENT_SECRET, config.APP_NAME)
