import subprocess
from handler_log.logger import loggerinfo, loggererror
from fastapi import APIRouter, Response, Body
from config.get_env import custom_env

drop = APIRouter()

@drop.post("/drop_base")
def backup_base(dbname: str = Body()):

    try:
        params = [
            '/usr/lib/postgresql/16/bin/dropdb',
            f'--no-password',
            f'{dbname}'
        ]

        subprocess.run(params, env = custom_env, text = True, check = True, capture_output = True)
        loggerinfo.info(f"База {dbname} успешно удалена")
        return Response(content = f"База {dbname} успешно удалена", media_type = "text/plain")
    except subprocess.CalledProcessError as err:
        loggererror.error(f"Ошибка выполнения команды: {err.stderr}")
        return Response(content = f"Ошибка выполнения команды, см. подробнее в error.log", media_type = "text/plain")