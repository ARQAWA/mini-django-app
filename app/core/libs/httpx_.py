from httpx import AsyncClient, Limits, Timeout

from app.core.libs.shutdown_container import shutdown_container

httpx_client = AsyncClient(
    limits=Limits(
        max_connections=100,
        max_keepalive_connections=70,
        keepalive_expiry=600,
    ),
    timeout=Timeout(
        timeout=7,
        connect=2,
    ),
)
shutdown_container.registry(httpx_client, "aclose")

__all__ = ["httpx_client"]
