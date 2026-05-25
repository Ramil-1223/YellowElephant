import pytest
import subprocess
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from core.drop_from_postgres import drop
from config.depends import get_run, get_env

app = FastAPI()
app.include_router(drop)
client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_overrides():
    yield
    app.dependency_overrides.clear()


def test_drop_base_success():
    mock_run = MagicMock()
    mock_run.return_value = MagicMock(returncode=0, stdout="Success", stderr="")

    fake_env = {"KEY": "value"}

    app.dependency_overrides[get_run] = lambda: mock_run
    app.dependency_overrides[get_env] = lambda: fake_env

    response = client.post("/drop_base", json="test_db")
    assert response.status_code == 200
    assert "База test_db успешно удалена" in response.text

    mock_run.assert_called_once_with(
        ["/usr/lib/postgresql/16/bin/dropdb", "--no-password", "test_db"],
        en=fake_env,
        text=True,
        check=True,
        capture_output=True,
    )


def test_drop_base_error():
    mock_run = MagicMock()
    mock_run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd="dropdb", stderr="database does not exist"
    )

    app.dependency_overrides[get_run] = lambda: mock_run
    app.dependency_overrides[get_env] = lambda: {}

    response = client.post("/drop_base", json="non_existent_db")
    assert response.status_code == 200
    assert "Ошибка выполнения команды, см. подробнее в error.log" in response.text
