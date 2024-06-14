from app.logic.tg_auth_validation import TgUser, get_user_object


async def process_user_auth(init_data: str) -> TgUser:
    """
    Получение данных пользователя.

    :param init_data: Данные инициализации
    :return: Словарь с данными пользователя.
    """
    return await get_user_object(init_data)
