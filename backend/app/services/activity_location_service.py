ACTIVITY_GEO_KEY = "activity:geo:recruiting"
ACTIVITY_LOCK_PREFIX = "activity:lock:"
ACTIVITY_LOCK_TTL_SECONDS = 3


def set_activity_geo(redis_client, activity_id: int, longitude: float, latitude: float) -> None:
    redis_client.geoadd(ACTIVITY_GEO_KEY, (longitude, latitude, str(activity_id)))


def remove_activity_geo(redis_client, activity_id: int) -> None:
    redis_client.zrem(ACTIVITY_GEO_KEY, str(activity_id))


def acquire_activity_lock(redis_client, activity_id: int) -> bool:
    key = f"{ACTIVITY_LOCK_PREFIX}{activity_id}"
    return bool(redis_client.set(key, "1", nx=True, ex=ACTIVITY_LOCK_TTL_SECONDS))


def release_activity_lock(redis_client, activity_id: int) -> None:
    redis_client.delete(f"{ACTIVITY_LOCK_PREFIX}{activity_id}")
