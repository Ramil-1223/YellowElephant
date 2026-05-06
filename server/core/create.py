import subprocess
from handler_log.logger import loggerinfo, loggererror
from fastapi import Response, Body, APIRouter
from config.get_env import custom_env
from config.schemas import CreateDB

create = APIRouter()

@create.post("/create_base")
def create_base(data: CreateDB = Body()):

    if data.cluster_id == "test":
        cluster_id = custom_env["ID_TEST_CLUSTER"]
        port =  custom_env["PORT_TEST"]
    elif data.cluster_id == "demo":
        cluster_id = custom_env["ID_DEMO_CLUSTER"]
        port = custom_env["PORT_DEMO"]

    try:
        params = [
            custom_env["RAC_PATH"],
            f'{custom_env["1C_HOST"]}:{port}',
            'infobase',
            'create',
            f'--cluster={cluster_id}',
            '--create-database',
            f'--name={data.dbname}',
            f'--descr={data.description}',
            '--dbms=PostgreSQL',
            f'--db-server={custom_env["PGHOST"]}',
            f'--db-name={data.dbname}',
            '--locale=ru',
            f'--db-user={custom_env["PGUSER"]}',
            f'--db-pwd={custom_env["PGPASSWORD"]}',
            '--license-distribution=allow',
            '--scheduled-jobs-deny=on',
            f'--cluster-user={custom_env["1C_USER"]}',
            f'--cluster-pwd={custom_env["1C_PASSWORD"]}'
        ]
        
        subprocess.run(params, check = True, text = True, capture_output = True)
        loggerinfo.info(f"База {data.dbname} успешно создана пользователем {data.description}.")
        return Response(content = f"База {data.dbname} успешно создана!", media_type = "text/plain")
    except subprocess.CalledProcessError as err:
        loggererror.error(f"Ошибка выполнения команды: {err.stderr}")
        return Response(content = f"Ошибка выполнения команды, см. подробнее в error.log", media_type = "text/plain")