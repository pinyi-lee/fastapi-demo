import redis.asyncio as redis

from app.manager.config import ConfigManager

class RedisManager:
    _redis_instance = None

    @classmethod
    async def init_redis(cls) -> None:
        try:
            if cls._redis_instance is None:
                cls._redis_instance = await redis.from_url(
                    f"redis://{ConfigManager.get_config().redis_host}:{ConfigManager.get_config().redis_port}",
                    db=0
                )
            await cls._redis_instance.ping()
        except Exception as e:
            raise RuntimeError(f"Init Redis Fail, Error: {e}")

    @classmethod
    def get_redis(cls) -> redis.Redis:
        if cls._redis_instance is None:
            raise RuntimeError("Redis instance is not initialized")
        return cls._redis_instance

    @classmethod
    async def close_redis(cls) -> None:
        if cls._redis_instance is not None:
            await cls._redis_instance.close()
            cls._redis_instance = None