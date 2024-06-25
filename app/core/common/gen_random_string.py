import random
import string

SYMBOLS = string.ascii_letters + string.digits + "#+-.@_|"


def sync_get_rand_string(length: int = 32) -> bytes:
    """Get the auth hash."""
    return "".join(random.choices(SYMBOLS, k=length)).encode()
