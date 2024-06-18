# from typing import Any, Literal
#
# import orjson
# import pytest
# from httpx import AsyncClient, Response
#
# # noinspection PyProtectedMember
# from httpx._client import USE_CLIENT_DEFAULT, UseClientDefault
#
# # noinspection PyProtectedMember
# from httpx._types import (
#     AuthTypes,
#     CookieTypes,
#     HeaderTypes,
#     QueryParamTypes,
#     RequestContent,
#     RequestData,
#     RequestExtensions,
#     RequestFiles,
#     TimeoutTypes,
#     URLTypes,
# )
# from redis.asyncio import Redis
#
# from app.core.asgi import application
#
#
# @pytest.fixture(scope="session")
# async def async_test_client() -> AsyncClient:
#     async with AsyncClient(app=application, base_url="http://test") as client:
#         yield client
#
#
# @pytest.fixture
# async def api_request(async_test_client):
#     async def _api_request(
#         method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
#         url: URLTypes,
#         *,
#         content: RequestContent | None = None,
#         data: RequestData | None = None,
#         files: RequestFiles | None = None,
#         json: Any | None = None,
#         params: QueryParamTypes | None = None,
#         headers: HeaderTypes | None = None,
#         cookies: CookieTypes | None = None,
#         auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
#         follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
#         timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
#         extensions: RequestExtensions | None = None,
#         user_token: str | None = None,
#     ) -> Response:
#         if user_token:
#             headers = headers or {}
#             headers["Authorization"] = f"Bearer {user_token}"
#         return await async_test_client.request(
#             method,
#             url,
#             content=content,
#             data=data,
#             files=files,
#             json=json,
#             params=params,
#             headers=headers,
#             cookies=cookies,
#             auth=auth,
#             follow_redirects=follow_redirects,
#             timeout=timeout,
#             extensions=extensions,
#         )
#
#     return _api_request
#
#
# @pytest.fixture(scope="session")
# async def __redis_client_session() -> Redis:
#     client = Redis.from_url("redis://redis-test/0")
#     try:
#         yield client
#     finally:
#         await client.aclose()
#
#
# from tests.http import api_request  # noqa
#
#
# @pytest.fixture
# async def get_user_token(redis):
#     async def _func(token: str, user_dict: dict) -> str:
#         await redis.set(token, orjson.dumps(user_dict))
#         return token
#
#     return _func
#
#
# @pytest.fixture
# async def redis(__redis_client_session) -> Redis:
#     await __redis_client_session.flushdb()
#     yield __redis_client_session
#     await __redis_client_session.flushdb()
