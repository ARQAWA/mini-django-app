# from tests.data.auth import USER_DICT, USER_TOKEN
#
#
# async def test_get_user_from_redis(api_request, get_user_token) -> None:
#     # When
#     token = await get_user_token(USER_TOKEN, USER_DICT)
#     response = await api_request("GET", "/api/v1/user/me", user_token=token)
#
#     # Then
#     assert response.status_code == 200, [repr(response.text), response]
#     assert response.json() == {"message": "Hello, world!"}
