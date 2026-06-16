import os
import json
from upstash_redis import Redis

# Upstash Redis Connection
redis_client = Redis(
    url=os.getenv("UPSTASH_REDIS_REST_URL"),
    token=os.getenv("UPSTASH_REDIS_REST_TOKEN")
)

CACHE_KEY = "users_cache"


def get_cached_users():
    """
    Fetch users from Redis cache
    Returns:
        (data, True)  -> if cache exists
        (None, False) -> if cache does not exist
    """
    try:
        cached_data = redis_client.get(CACHE_KEY)

        if cached_data:
            # Handle both string and object responses
            if isinstance(cached_data, str):
                return json.loads(cached_data), True

            return cached_data, True

        return None, False

    except Exception as e:
        print(f"Redis error: {e}")
        return None, False


def set_cached_users(users_data):
    """
    Store users in Redis cache
    """
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
    """
    Clear users cache
    """
    try:
        redis_client.delete(CACHE_KEY)
        return True

    except Exception as e:
        print(f"Redis cache clear error: {e}")
        return False


def redis_connection_test():
    """
    Test Upstash Redis connection
    """
    try:
        redis_client.set("health_check", "ok")
        value = redis_client.get("health_check")

        return value == "ok"

    except Exception as e:
        print(f"Redis connection error: {e}")
        return False
