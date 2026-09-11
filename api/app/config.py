import os


class Settings:
    def __init__(self) -> None:
        self.database_url = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://app:app@localhost:5432/projects_stacks",
        )
        cors = os.getenv("CORS_ORIGINS", "*")
        self.cors_origins = [origin.strip() for origin in cors.split(",") if origin.strip()]


def get_settings() -> Settings:
    return Settings()