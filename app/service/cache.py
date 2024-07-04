import redis

from config.config import get_config as config

redis_instance = None

def get_redis():
    global redis_instance
    if redis_instance is None:
        redis_instance = redis.Redis(host=config().redis_host, port=config().redis_port, db=0)
    return redis_instance