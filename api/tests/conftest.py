import pytest
from fastapi.testclient import TestClient

from app.database import Base
from app.main import create_app


@pytest.fixture()
def client() -> TestClient:
    app = create_app(db_url="sqlite://")
    Base.metadata.create_all(app.state.engine)
    with TestClient(app) as test_client:
        yield test_client