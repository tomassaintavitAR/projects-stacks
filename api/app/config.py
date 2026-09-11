import os


class Settings:
    def __init__(self) -> None:
        raw_url = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://app:app@localhost:5432/projects_stacks",
        )
        if raw_url.startswith("postgres://"):
            raw_url = "postgresql+psycopg://" + raw_url[len("postgres://") :]
        elif raw_url.startswith("postgresql://"):
            raw_url = "postgresql+psycopg://" + raw_url[len("postgresql://") :]
        self.database_url = raw_url
        cors = os.getenv("CORS_ORIGINS", "*")
        self.cors_origins = [origin.strip() for origin in cors.split(",") if origin.strip()]


def get_settings() -> Settings:
    return Settings()