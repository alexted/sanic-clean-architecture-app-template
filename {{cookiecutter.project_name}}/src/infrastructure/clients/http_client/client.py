import json as jsonlib
import typing as t
import logging
from functools import reduce

import httpx

logger = logging.getLogger()

Middleware = list[t.Callable[[t.Any, t.Callable], t.Any]] | None


def strip_none(**kwargs: str) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}


def handler_factory(handler: t.Callable, middleware: t.Callable) -> t.Callable:
    async def handle(data: dict) -> dict:
        return await middleware(data, handler)

    return handle


class HttpClient:
    def __init__(
        self,
        base_url: str,
        query_params: dict = None,
        headers: dict = None,
        verify: bool = False,
        **session_params: dict,
    ) -> None:
        self._base_url: str = base_url
        self._query_params: dict = query_params
        self._headers: dict = headers
        self._verify: bool = verify
        self._session_params: dict = session_params
        self.__session: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "HttpClient":
        return self

    async def __aexit__(self, exc_type: str, exc_val: str, exc_tb: str) -> None:
        await self.close()

    async def close(self) -> None:
        session, self.__session = self.__session, None
        if session:
            await session.aclose()

    @property
    def _session(self) -> httpx.AsyncClient:
        if self.__session is None:
            self.__session: httpx.AsyncClient = httpx.AsyncClient(
                base_url=self._base_url,
                params=self._query_params,
                headers=self._headers,
                verify=self._verify,
                **self._session_params,
            )

        return self.__session

    async def call(  # noqa: CFQ002
        self,
        path: str = "",
        method: str = "GET",
        data: dict = None,
        json: dict = None,
        params: dict = None,
        headers: dict = None,
        timeout: int = None,
        files: bytes = None,
        **kwargs: dict,
    ) -> httpx.Response:
        """
        Call the API method of the infrastructure. Repeats the interface of the request method of the httpx library

        :param path:
        :param method:
        :param data:
        :param json:
        :param files:
        :param params:
        :param headers:
        :param timeout:
        :return: httpx.Response
        """

        if json is not None:
            if isinstance(json, str):
                data: str = json
            else:
                data: bytes = jsonlib.dumps(json, ensure_ascii=False).encode("utf-8")

            if headers:
                if "content-type" not in headers:
                    headers["content-type"] = "application/json"
            else:
                headers = {"content-type": "application/json"}

        logger.debug(
            f"request: [{method}] {str(self._session.base_url) + path}\n"
            f"params: {params}\n"
            f"data: {data}\n"
            f"headers: {headers}"
        )

        response: httpx.Response = await self._session.request(
            url=path, method=method, data=data, headers=headers, params=params, timeout=timeout, files=files, **kwargs
        )

        logger.debug(f"response: [{response.status_code}] {response.content}")

        return response


class ApiCall:
    def __init__(self, client: HttpClient, path: str = "", method: str = "GET", middleware: Middleware = None) -> None:
        self._client: HttpClient = client
        self._path: str = path
        self._method: str = method
        self._handler: t.Callable = reduce(handler_factory, (middleware or [])[::-1], self._call)

    async def _call(self, parameters: dict) -> httpx.Response:
        path_params: dict = parameters.pop("path_params", {})
        path: str = self._path.format(**path_params) if path_params else self._path

        headers: dict = {**(self._client._session.headers or {}), **(parameters.get("headers") or {})}

        if headers:
            parameters["headers"] = headers

        parameters.update({"method": self._method})

        return await self._client.call(path=path, **parameters)

    async def __call__(  # noqa: CFQ002
        self,
        data: dict = None,
        json: dict = None,
        params: dict = None,
        path_params: dict = None,
        headers: dict = None,
        **kwargs: dict,
    ) -> t.Any:  # noqa ANN401
        return await self._handler(
            strip_none(data=data, json=json, params=params, path_params=path_params, headers=headers, **kwargs)
        )
