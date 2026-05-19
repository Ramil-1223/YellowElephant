import subprocess, re
from fastapi import APIRouter, Response, Body
from config.get_env import custom_env
from handler_log.logger import loggerinfo, loggererror
from config.schemas import DropDB1C


drop_1C = APIRouter()

@drop_1C.post("/drop_base_1C")
def get_list(data: DropDB1C = Body()):
    
    if data.cluster == "test":
        cluster_id = custom_env["ID_TEST_CLUSTER"]
        port =  custom_env["PORT_TEST"]
    elif data.cluster == "demo":
        cluster_id = custom_env["ID_DEMO_CLUSTER"]
        port = custom_env["PORT_DEMO"]
    else:
        raise ValueError("Кластер не найден")

    get_list = [
        custom_env["RAC_PATH"],
        f'{custom_env["1C_HOST"]}:{port}',
        'infobase',
        'summary',
        'list',
        f'--cluster={cluster_id}',
        f'--cluster-user={custom_env["1C_USER"]}',
        f'--cluster-pwd={custom_env["1C_PASSWORD"]}'
    ]

    list_base = subprocess.run(get_list, text = True, check = True, capture_output = True)

    pattern = (
        r"infobase\s*:\s*(?P<infobase>[a-f0-9-]{36})\s*\n"
        r"name\s*:\s*(?P<name>[^\s\n]+)\s*\n"
        # r"descr\s*:\s*.*"
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
            custom_env["RAC_PATH"],
            f'{custom_env["1C_HOST"]}:{port}',
            'infobase',
            'drop',
            f'--cluster={cluster_id}',
            f'--infobase={dict_idbase[data.dbname]}',
            f'--cluster-user={custom_env["1C_USER"]}',
            f'--cluster-pwd={custom_env["1C_PASSWORD"]}'
        ]

        subprocess.run(drop_base1C, check = True, text = True, capture_output = True)
        loggerinfo.info(f"База данных {data.dbname} успешно удалена из кластера {data.cluster}.")
        return Response(content = f"База данных {data.dbname} успешно удалена из кластера {data.cluster}", media_type = "text/plain")
    except subprocess.CalledProcessError as err:
        loggererror.error(f"Ошибка выполнения команды: {err.stderr}")
        return Response(content = f"Ошибка выполнения команды, см. подробнее в error.log", media_type = "text/plain")