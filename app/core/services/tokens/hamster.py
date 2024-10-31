import urllib.parse


def get_raw_init_data(init_data: str) -> str:
    """Получение raw_init_data для игры Hamster Kombat."""
    init_data = urllib.parse.unquote(init_data)
    qs = urllib.parse.parse_qs(init_data, strict_parsing=True)

    new_qs = {k: v[0] for k, v in qs.items() if k in {"query_id", "user", "auth_date", "hash"}}

    return urllib.parse.urlencode(new_qs)
