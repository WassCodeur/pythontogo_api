from pydantic import BaseModel


class Config(BaseModel):
    """Config schema for the application."""

    env: str = "development"
    app_name: str = "Python Togo API V2.1.0"
    business_name: str = "Python Software Community of Togo"
    debug: bool = False
    base_url: str = "http://localhost:8008"
    root_path: str = "/api/v2"
    db_url: str = "sqlite:///./test.db"
    db_name: str = "test.db"
    db_user: str = "user"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: int = 5432
    redis_url: str = "redis://localhost:6379/2"
    secret_key: str = "your_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    log_level: str = "info"
    smtp_server: str = "smtp.example.com"
    smtp_port: int = 587
    smtp_user: str = "user"
    smtp_password: str = "password"
    paydunya_public_key: str
    paydunya_private_key: str
    paydunya_token: str
    paydunya_master_key: str
