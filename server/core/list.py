import re
from fastapi import APIRouter, Response, Body, Depends
from config.depends import get_env, get_run

ls = APIRouter()


@ls.post("/list_base")
def get_list(cluster: str = Body(),
             run = Depends(get_run),
             env = Depends(get_env)):
    
    if cluster == "test":
        cluster_id = env["ID_TEST_CLUSTER"]
        port =  env["PORT_TEST"]
    elif cluster == "demo":
        cluster_id = env["ID_DEMO_CLUSTER"]
        port = env["PORT_DEMO"]
    else:
        raise ValueError("Кластер не найден")

    params = [
        env["RAC_PATH"],
        f'{env["1C_HOST"]}:{port}',
        'infobase',
        'summary',
        'list',
        f'--cluster={cluster_id}',
        f'--cluster-user={env["1C_USER"]}',
        f'--cluster-pwd={env["1C_PASSWORD"]}'
    ]

    list_base = run(params, text = True, check = True, capture_output = True)

    pattern = (
        r"infobase\s*:\s*(?P<infobase>[a-f0-9-]{36})\s*\n"
        r"name\s*:\s*(?P<name>[^\s\n]+)\s*\n"
        r"(?:\s*\n\s*descr\s*:\s*.*)?"
    )

    matches = re.finditer(pattern, list_base.stdout, re.MULTILINE)
    infobases = [match.groupdict() for match in matches]
    list_bases = [item['name'] for item in infobases]
    str_base = '\n'.join(list_bases)

    return Response(content = str_base, media_type = "text/plain")