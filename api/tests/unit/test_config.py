import pytest

from app.config import Settings


def test_default_database_url(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert Settings().database_url == "postgresql+psycopg://app:app@localhost:5432/projects_stacks"


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (
            "postgresql://postgres.abc:pass@host:6543/postgres?sslmode=require",
            "postgresql+psycopg://postgres.abc:pass@host:6543/postgres?sslmode=require",
        ),
        (
            "postgres://postgres.abc:pass@host:6543/postgres?sslmode=require",
            "postgresql+psycopg://postgres.abc:pass@host:6543/postgres?sslmode=require",
        ),
        (
            "postgresql+psycopg://app:app@localhost:5432/projects_stacks",
            "postgresql+psycopg://app:app@localhost:5432/projects_stacks",
        ),
        ("sqlite://", "sqlite://"),
    ],
)
def test_database_url_normalization(monkeypatch, raw: str, expected: str) -> None:
    monkeypatch.setenv("DATABASE_URL", raw)
    assert Settings().database_url == expected