USER_GEO_KEY = "user:geo"
USER_ONLINE_PREFIX = "user:online:"
USER_ONLINE_TTL_SECONDS = 300


def set_user_geo(redis_client, user_id: int, longitude: float, latitude: float) -> None:
    redis_client.geoadd(USER_GEO_KEY, (longitude, latitude, str(user_id)))


def set_user_online(redis_client, user_id: int) -> None:
    redis_client.setex(f"{USER_ONLINE_PREFIX}{user_id}", USER_ONLINE_TTL_SECONDS, "1")
