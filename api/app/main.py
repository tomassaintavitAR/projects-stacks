from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models  # noqa: F401  (register models on Base.metadata)
from app.config import get_settings
from app.database import create_engine_and_session
from app.routers import projects, technologies


def create_app(db_url: str | None = None) -> FastAPI:
    settings = get_settings()
    engine, session_factory = create_engine_and_session(db_url or settings.database_url)

    application = FastAPI(title="Project Stacks API", version="0.1.0")
    application.state.engine = engine
    application.state.session_factory = session_factory

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(projects.router)
    application.include_router(technologies.router)

    @application.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()