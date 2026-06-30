from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "coffe_house"
    app_env: str = "local"
    app_debug: bool = True
    
    
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    auth_access_cookie_name: str = "access_token"
    auth_cookie_httponly: bool = True
    auth_cookie_secure: bool = False
    auth_cookie_samesite: str = "lax"
    auth_cookie_path: str = "/"
    
    
    postgres_host: str
    postgres_port: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    
    database_url: str
    
    
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    redis_url: str = "redis://redis:6379/0"
    
    redis_key_prefix: str = "coffee_house"
    
    auth_login_rate_limit: int = 5
    auth_login_limit_window_seconds: int = 60
    auth_register_rate_limit: int = 3
    auth_register_rate_limit_window_seconds: int = 300
    
    catalog_cache_ttl_seconds: int = 60
    
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()