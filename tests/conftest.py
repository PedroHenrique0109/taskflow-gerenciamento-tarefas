import pytest
from src.app import create_app


@pytest.fixture
def app(tmp_path):
    database_path = tmp_path / 'test_taskflow.db'
    app = create_app({'DATABASE_PATH': database_path})
    app.config.update({'TESTING': True})
    return app


@pytest.fixture
def client(app):
    return app.test_client()
