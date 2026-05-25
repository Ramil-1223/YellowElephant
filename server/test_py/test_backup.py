import pytest, subprocess
from datetime import datetime
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from config.depends import get_run, get_env
from core.backup import backup

app = FastAPI()
app.include_router(backup)
client = TestClient(app)

@pytest.fixture(autouse = True)
def cleanup_overrides():
    yield
    app.dependency_overrides.clear()


# @patch('core.backup.datetime')
def test_backup_base_directory_format_success():
    today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    mock_run = MagicMock()
    mock_run.return_value = MagicMock(returncode = 0)
    fake_env = {"PGPASSWORD": "password"}
    
    app.dependency_overrides[get_run] = lambda: mock_run
    app.dependency_overrides[get_env] = lambda: fake_env
    
    payload = {
        "dbname": "prod_db",
        "backup_dir": "/var/backups",
        "backup_format": "directory"
    }
    
    response = client.post("/backup_base", json = payload)
    
    assert response.status_code == 200
    assert "успешно выполнена" in response.text
    assert f"/var/backups/prod_db_{today}.backup" in response.text
    
    mock_run.assert_called_once_with(
        [
            '/usr/lib/postgresql/16/bin/pg_dump',
            '--no-password',
            '--format=d',
            f'--file=/var/backups/prod_db_{today}.backup',
            'prod_db'
        ],
        env = fake_env,
        text = True,
        check = True,
        capture_output = True
    )


@pytest.mark.parametrize("input_format, expected_flag, expected_ext", [
    ("custom", "c", ".custom"),
    ("tar", "t", ".tar"),
    ("plain-text", "p", ".sql"),
])


def test_backup_base_other_formats(input_format, expected_flag, expected_ext):
    today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    mock_run = MagicMock()
    
    app.dependency_overrides[get_run] = lambda: mock_run
    app.dependency_overrides[get_env] = lambda: {}
    
    payload = {
        "dbname": "prod_db",
        "backup_dir": "/var/backups",
        "backup_format": input_format
    }
    
    response = client.post("/backup_base", json = payload)
    
    assert response.status_code == 200
    
    called_args = mock_run.call_args[0][0]
    assert f'--format={expected_flag}' in called_args
    assert f'--file=/var/backups/prod_db_{today}{expected_ext}' in called_args


def test_backup_base_subprocess_error():
    mock_run = MagicMock()
    mock_run.side_effect = subprocess.CalledProcessError(
        returncode = 1,
        cmd = 'pg_dump',
        stderr = "pg_dump: error: connection to server on socket failed"
    )
    
    app.dependency_overrides[get_run] = lambda: mock_run
    app.dependency_overrides[get_env] = lambda: {}
    
    payload = {
        "dbname": "prod_db",
        "backup_dir": "/var/backups",
        "backup_format": "tar"
    }
    
    response = client.post("/backup_base", json = payload)
    
    assert response.status_code == 200
    assert "Ошибка выполнения команды, см. подробнее в errors.log" in response.text