import subprocess, re
from fastapi import APIRouter, Response, Body, Depends
from config.depends import get_env, get_run
from handler_log.logger import loggerinfo, loggererror
from config.schemas import DropDB1C


drop_1C = APIRouter()

@drop_1C.post("/drop_base_1C")
def drop_base1C(data: DropDB1C = Body(),
                run = Depends(get_run),
                env = Depends(get_env)):
    
    if data.cluster == "test":
        cluster_id = env["ID_TEST_CLUSTER"]
        port =  env["PORT_TEST"]
    elif data.cluster == "demo":
        cluster_id = env["ID_DEMO_CLUSTER"]
        port = env["PORT_DEMO"]
    else:
        raise ValueError("Кластер не найден")

    get_list = [
        env["RAC_PATH"],
        f'{env["1C_HOST"]}:{port}',
        'infobase',
        'summary',
        'list',
        f'--cluster={cluster_id}',
        f'--cluster-user={env["1C_USER"]}',
        f'--cluster-pwd={env["1C_PASSWORD"]}'
    ]

    list_base = run(get_list, text = True, check = True, capture_output = True)

    pattern = (
        r"infobase\s*:\s*(?P<infobase>[a-f0-9-]{36})\s*\n"
        r"name\s*:\s*(?P<name>[^\s\n]+)\s*\n"
        r"(?:\s*\n\s*descr\s*:\s*.*)?"
    )

    matches = re.finditer(pattern, list_base.stdout, re.MULTILINE)
    infobases = [match.groupdict() for match in matches]
    dict_idbase = {item['name']: item['infobase'] for item in infobases}

    if data.dbname not in dict_idbase:
        loggererror.error(f"Базы {data.dbname} не существует в кластере {data.cluster}!")
        return Response(content = f"Базы {data.dbname} не существует в кластере {data.cluster}!", media_type = "text/plain")

    try:
        drop_base1C = [
            env["RAC_PATH"],
            f'{env["1C_HOST"]}:{port}',
            'infobase',
            'drop',
            f'--cluster={cluster_id}',
            f'--infobase={dict_idbase[data.dbname]}',
            f'--cluster-user={env["1C_USER"]}',
            f'--cluster-pwd={env["1C_PASSWORD"]}'
        ]

        run(drop_base1C, check = True, text = True, capture_output = True)
        loggerinfo.info(f"База данных {data.dbname} успешно удалена из кластера {data.cluster}.")
        return Response(content = f"База данных {data.dbname} успешно удалена из кластера {data.cluster}", media_type = "text/plain")
    except subprocess.CalledProcessError as err:
        loggererror.error(f"Ошибка выполнения команды: {err.stderr}")
        return Response(content = f"Ошибка выполнения команды, см. подробнее в error.log", media_type = "text/plain")