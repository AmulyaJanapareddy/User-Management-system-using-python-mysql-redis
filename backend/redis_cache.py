import redis
import json
from config import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_cached_users():
    try:
        cached_data = redis_client.get("users_cache")
        if cached_data:
            return json.loads(cached_data), True
        return None, False
    except Exception as e:
        print(f"Redis error: {e}")
        return None, False

def set_cached_users(users_data):
    try:
        redis_client.set("users_cache", json.dumps(users_data))
        return True
    except Exception as e:
        print(f"Redis cache set error: {e}")
        return False

def clear_cache():
    try:
        redis_client.delete("users_cache")
        return True
    except Exception as e:
        print(f"Redis cache clear error: {e}")
        return False

def redis_connection_test():
    try:
        redis_client.ping()
        return True
    except Exception as e:
        print(f"Redis connection error: {e}")
        return False
