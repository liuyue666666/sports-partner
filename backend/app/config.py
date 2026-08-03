from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "sports-partner"
    app_env: str = "development"
    app_debug: bool = True
    app_secret_key: str = "change-me"

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "sports_partner"
    mysql_password: str = "sports_partner"
    mysql_database: str = "sports_partner"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""

    jwt_secret_key: str = "change-me-jwt"
    jwt_access_token_expire_minutes: int = 120
    jwt_refresh_token_expire_days: int = 7

    wechat_app_id: str = ""
    wechat_app_secret: str = ""

    match_default_radius_meters: int = 5000
    match_weight_distance: float = 0.4
    match_weight_sport: float = 0.4
    match_weight_time: float = 0.2

    cors_origins: str = "http://localhost:5173"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
            "?charset=utf8mb4"
        )

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
