import subprocess
from datetime import datetime
from fastapi import APIRouter, Response, Body, Depends
from handler_log.logger import loggerinfo, loggererror
from config.depends import get_env, get_run
from config.schemas import BackupDB


backup = APIRouter()


@backup.post("/backup_base")
def backup_base(data: BackupDB = Body(),
                run = Depends(get_run),
                env = Depends(get_env)):
    
    today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if data.backup_format == "directory":
        form_backup = "d"
        extension = ".backup"
    elif data.backup_format == "custom":
        form_backup = "c"
        extension = ".custom"
    elif data.backup_format == "tar":
        form_backup = "t"
        extension = ".tar"
    elif data.backup_format == "plain-text":
        form_backup = "p"
        extension = ".sql"
    else:
        raise ValueError("Некорректный формат бэкапа")

    try:
        params = [
            '/usr/lib/postgresql/16/bin/pg_dump',
            f'--no-password',
            f'--format={form_backup}',
            f'--file={data.backup_dir}/{data.dbname}_{today}{extension}',
            f'{data.dbname}'
        ]

        run(params, env = env, text = True, check = True, capture_output = True)
        loggerinfo.info(f"Резервная копия базы {data.dbname} успешно выполнена в директорию по пути {data.backup_dir}/{data.dbname}_{today}{extension}")
        return Response(content = f"Резервная копия базы {data.dbname} успешно выполнена в директорию по пути {data.backup_dir}/{data.dbname}_{today}{extension}", media_type = "text/plain")
    except subprocess.CalledProcessError as err:
        loggererror.error(f"Ошибка выполнения команды: {err.stderr}")
        return Response(content = f"Ошибка выполнения команды, см. подробнее в errors.log", media_type = "text/plain")