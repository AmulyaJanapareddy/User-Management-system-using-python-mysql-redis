import json
from upstash_redis import Redis

redis_client = Redis(
    url="https://strong-monster-149801.upstash.io",
    token="YOUR_UPSTASH_TOKEN"
)

CACHE_KEY = "users_cache"


def get_cached_users():
    try:
        cached_data = redis_client.get(CACHE_KEY)

        if cached_data:
            if isinstance(cached_data, str):
                return json.loads(cached_data), True
            return cached_data, True

        return None, False

    except Exception as e:
        print(f"Redis error: {e}")
        return None, False


def set_cached_users(users_data):
    try:
        redis_client.set(
            CACHE_KEY,
            json.dumps(users_data)
        )
        return True

    except Exception as e:
        print(f"Redis cache set error: {e}")
        return False


def clear_cache():
    try:
        redis_client.delete(CACHE_KEY)
        return True

    except Exception as e:
        print(f"Redis cache clear error: {e}")
        return False


def redis_connection_test():
    try:
        redis_client.set("health_check", "ok")
        value = redis_client.get("health_check")

        return value == "ok"

    except Exception as e:
        print(f"Redis connection error: {e}")
        return False
