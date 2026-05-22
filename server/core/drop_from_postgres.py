import subprocess
from handler_log.logger import loggerinfo, loggererror
from fastapi import APIRouter, Response, Body, Depends
from config.depends import get_env, get_run

drop = APIRouter()


@drop.post("/drop_base")
def drop_base(dbname: str = Body(),
              run = Depends(get_run),
              env = Depends(get_env)):

    try:
        params = [
            '/usr/lib/postgresql/16/bin/dropdb',
            '--no-password',
            f'{dbname}'
        ]

        run(params, env = env, text = True, check = True, capture_output = True)
        loggerinfo.info(f"База {dbname} успешно удалена")
        return Response(content = f"База {dbname} успешно удалена", media_type = "text/plain")
    except subprocess.CalledProcessError as err:
        loggererror.error(f"Ошибка выполнения команды: {err.stderr}")
        return Response(content = f"Ошибка выполнения команды, см. подробнее в error.log", media_type = "text/plain")