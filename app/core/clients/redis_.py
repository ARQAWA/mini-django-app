from redis.asyncio import ConnectionPool, Redis

from app.core.envs import envs

redis_client = Redis.from_pool(ConnectionPool.from_url(envs.redis.dsn))
