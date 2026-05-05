import subprocess
from handler_log.logger import loggerinfo, loggererror
from fastapi import Response, Body, APIRouter
from config.get_env import custom_env


create = APIRouter()

@create.post("/create_base")
def create_base(
        description: str = Body(), 
        port: str = Body(), 
        cluster_id: str = Body(), 
        dbname: str = Body()
    ) -> str:


    if cluster_id == "test":
        cluster_id = custom_env["ID_TEST_CLUSTER"]
        port =  custom_env["PORT_TEST"]
    elif cluster_id == "demo":
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
            f'--name={dbname}',
            f'--descr={description}',
            '--dbms=PostgreSQL',
            f'--db-server={custom_env["PGHOST"]}',
            f'--db-name={dbname}',
            '--locale=ru',
            f'--db-user={custom_env["PGUSER"]}',
            f'--db-pwd={custom_env["PGPASSWORD"]}',
            '--license-distribution=allow',
            '--scheduled-jobs-deny=on',
            f'--cluster-user={custom_env["1C_USER"]}',
            f'--cluster-pwd={custom_env["1C_PASSWORD"]}'
        ]
        
        subprocess.run(params, check = True, text = True, capture_output = True)
        loggerinfo.info(f"База {dbname} успешно создана пользователем {description}.")
        return Response(content = f"База {dbname} успешно создана!", media_type = "text/plain")
    except subprocess.CalledProcessError as err:
        loggererror.error(f"Ошибка выполнения команды: {err.stderr}")
        return Response(content = f"Ошибка выполнения команды, см. подробнее в error.log", media_type = "text/plain")