import redis

redis_instance = None

def get_redis():
    global redis_instance
    if redis_instance is None:
        redis_instance = redis.Redis(host='localhost', port=6379, db=0)
    return redis_instance