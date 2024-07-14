import urllib.parse
from typing import Any


def decode_initdata(initdata: str) -> dict[str, Any]:
    """
    Функция декодирования initdata.

    :param initdata: строка initdata
    :return: словарь initdata.
    """
    initdata_query = urllib.parse.unquote(urllib.parse.unquote(initdata))

    result = {
        key: value[0] if len(value) == 1 else value for key, value in urllib.parse.parse_qs(initdata_query).items()
    }

    return result
