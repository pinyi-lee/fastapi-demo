import redis

from config.config import ConfigManager

class RedisManager:
    _redis_instance = None

    @classmethod
    def init_redis(cls) -> None:
        try:
            if cls._redis_instance is None:
                cls._redis_instance = redis.Redis(host=ConfigManager.get_config().redis_host, port=ConfigManager.get_config().redis_port, db=0)
            cls._redis_instance.ping()
        except Exception as e:
            raise RuntimeError(f"Init Redis Fail, Error: {e}")
    
    @classmethod
    def get_redis(cls) -> redis.Redis:
        return cls._redis_instance

    @classmethod
    def close_redis(cls) -> None:
        if cls._redis_instance is not None:
            cls._redis_instance.close()
            cls._redis_instance = None