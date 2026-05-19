import re, subprocess
from fastapi import APIRouter, Response, Body
from config.get_env import custom_env


ls = APIRouter()

@ls.post("/list_base")
def get_list(cluster: str = Body()):
    
    if cluster == "test":
        cluster_id = custom_env["ID_TEST_CLUSTER"]
        port =  custom_env["PORT_TEST"]
    elif cluster == "demo":
        cluster_id = custom_env["ID_DEMO_CLUSTER"]
        port = custom_env["PORT_DEMO"]
    else:
        raise ValueError("Кластер не найден")

    params = [
        custom_env["RAC_PATH"],
        f'{custom_env["1C_HOST"]}:{port}',
        'infobase',
        'summary',
        'list',
        f'--cluster={cluster_id}',
        f'--cluster-user={custom_env["1C_USER"]}',
        f'--cluster-pwd={custom_env["1C_PASSWORD"]}'
    ]

    result = subprocess.run(params, text = True, check = True, capture_output = True)
    return get_parsed_infobases(result.stdout)


def get_parsed_infobases(list_base: str):

    pattern = (
        r"infobase\s*:\s*(?P<infobase>[a-f0-9-]{36})\s*\n"
        r"name\s*:\s*(?P<name>[^\s\n]+)\s*\n"
        r"descr\s*:\s*.*"
    )

    matches = re.finditer(pattern, list_base, re.MULTILINE)
    infobases = [match.groupdict() for match in matches]
    list_bases = [item['name'] for item in infobases]
    str_base = '\n'.join(list_bases)

    return Response(content = str_base, media_type = "text/plain")