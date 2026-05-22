import subprocess
from handler_log.logger import loggerinfo, loggererror
from fastapi import Response, Body, APIRouter, Depends
from config.depends import get_env, get_run
from config.schemas import CreateDB


create = APIRouter()

@create.post("/create_base")
def create_base(data: CreateDB = Body(),
              run = Depends(get_run),
              env = Depends(get_env)):

    if data.cluster_id == "test":
        cluster_id = env["ID_TEST_CLUSTER"]
        port =  env["PORT_TEST"]
    elif data.cluster_id == "demo":
        cluster_id = env["ID_DEMO_CLUSTER"]
        port = env["PORT_DEMO"]
    else:
        raise ValueError("Кластер не найден")

    try:
        params = [
            env["RAC_PATH"],
            f'{env["1C_HOST"]}:{port}',
            'infobase',
            'create',
            f'--cluster={cluster_id}',
            '--create-database',
            f'--name={data.dbname}',
            f'--descr={data.description}',
            '--dbms=PostgreSQL',
            f'--db-server={env["PGHOST"]}',
            f'--db-name={data.dbname}',
            '--locale=ru',
            f'--db-user={env["PGUSER"]}',
            f'--db-pwd={env["PGPASSWORD"]}',
            '--license-distribution=allow',
            '--scheduled-jobs-deny=on',
            f'--cluster-user={env["1C_USER"]}',
            f'--cluster-pwd={env["1C_PASSWORD"]}'
        ]
        
        run(params, check = True, text = True, capture_output = True)
        loggerinfo.info(f"База {data.dbname} успешно создана пользователем {data.description}.")
        return Response(content = f"База {data.dbname} успешно создана!", media_type = "text/plain")
    except subprocess.CalledProcessError as err:
        loggererror.error(f"Ошибка выполнения команды: {err.stderr}")
        return Response(content = f"Ошибка выполнения команды, см. подробнее в error.log", media_type = "text/plain")