# app/core/config.py

class Settings:
    # JWT / auth settings
    SECRET_KEY: str = "supersecretkey_change_me"  # 🚨 change this in real projects
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour

    # MySQL database config
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "tarun200727"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = "smart_spending"


# Single global settings instance
settings = Settings()
