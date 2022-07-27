from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOSTNAME: str = "localhost"
    DB_PORT: str = "5432"
    DB_PASSWORD: str = "123456"
    DB_NAME: str = "fastapi"
    USERNAME: str = "postgres"
    SECRET_KEY: str = "09bhdfgvdhfdbn873bgv784bhb4802ub3h4888230"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 100

    class Config:
        env_file = ".env"


settings = Settings()
