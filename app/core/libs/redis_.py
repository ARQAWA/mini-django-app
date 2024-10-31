from redis.asyncio import ConnectionPool, Redis

from app.core.envs import envs
from app.core.libs.shutdown_container import shutdown_container

redis_client = Redis.from_pool(ConnectionPool.from_url(envs.redis.dsn))
shutdown_container.registry(redis_client, "close")

__all__ = ["redis_client"]
