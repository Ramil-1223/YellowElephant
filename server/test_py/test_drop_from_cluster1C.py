import pytest
import subprocess
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from core.drop_from_cluster1C import drop_1C
from config.depends import get_run, get_env


app = FastAPI()
app.include_router(drop_1C)
client = TestClient(app)

@pytest.fixture(autouse = True)
def cleanup_overrides():
    yield
    app.dependency_overrides.clear()


def test_drop_base_1c_success():
    fake_env = {
        "ID_TEST_CLUSTER": "cluster-1111", 
        "PORT_TEST": "1540",
        "RAC_PATH": "rac", 
        "1C_HOST": "localhost",
        "1C_USER": "admin", 
        "1C_PASSWORD": "pwd"
    }
    

    fake_rac_list_stdout = (
        "infobase : 4b2f4b2f-4b2f-4b2f-4b2f-4b2f4b2f4b2f\n"
        "name     : test_db\n"
        "descr    : Управление торговлей\n"
    )
    
    mock_run = MagicMock()
    mock_run.side_effect = [
        MagicMock(returncode = 0, stdout = fake_rac_list_stdout),
        MagicMock(returncode = 0, stdout = "")
    ]
    
    app.dependency_overrides[get_run] = lambda: mock_run
    app.dependency_overrides[get_env] = lambda: fake_env
    
    payload = {"cluster": "test", "dbname": "test_db"}
    response = client.post("/drop_base_1C", json = payload)
    
    assert response.status_code == 200
    assert "успешно удалена из кластера" in response.text
    assert mock_run.call_count == 2
    
    second_call_args = mock_run.call_args_list[1][0][0]
    assert "--infobase=4b2f4b2f-4b2f-4b2f-4b2f-4b2f4b2f4b2f" in second_call_args


def test_drop_base_1c_not_found():
    fake_env = {
        "ID_TEST_CLUSTER": "cluster-1111", 
        "PORT_TEST": "1540",
        "RAC_PATH": "rac", 
        "1C_HOST": "localhost",
        "1C_USER": "admin", 
        "1C_PASSWORD": "pwd"
    }
    
    fake_rac_list_stdout = (
        "infobase : 00000000-0000-0000-0000-000000000000\n"
        "name     : other_db\n"
    )
    
    mock_run = MagicMock()

    mock_run.return_value = MagicMock(returncode = 0, stdout = fake_rac_list_stdout)
    
    app.dependency_overrides[get_run] = lambda: mock_run
    app.dependency_overrides[get_env] = lambda: fake_env
    
    payload = {"cluster": "test", "dbname": "trade_db"}
    response = client.post("/drop_base_1C", json = payload)
    
    assert response.status_code == 200
    assert "не существует в кластере" in response.text
    assert mock_run.call_count == 1


def test_drop_base_1c_subprocess_error():
    fake_env = {
        "ID_TEST_CLUSTER": "cluster-1111", 
        "PORT_TEST": "1540",
        "RAC_PATH": "rac", 
        "1C_HOST": "localhost",
        "1C_USER": "admin", 
        "1C_PASSWORD": "pwd"
    }
    
    fake_rac_list_stdout = (
        "infobase : 4b2f4b2f-4b2f-4b2f-4b2f-4b2f4b2f4b2f\n"
        "name     : trade_db\n"
    )
    
    mock_run = MagicMock()

    mock_run.side_effect = [
        MagicMock(returncode = 0, stdout = fake_rac_list_stdout),
        subprocess.CalledProcessError(
            returncode = 1, 
            cmd = 'rac infobase drop', 
            stderr = "Authentication failed: bad password"
        )
    ]
    
    app.dependency_overrides[get_run] = lambda: mock_run
    app.dependency_overrides[get_env] = lambda: fake_env
    
    payload = {"cluster": "test", "dbname": "trade_db"}
    response = client.post("/drop_base_1C", json = payload)
    
    assert response.status_code == 200
    assert "Ошибка выполнения команды, см. подробнее в error.log" in response.text
    
    assert mock_run.call_count == 2