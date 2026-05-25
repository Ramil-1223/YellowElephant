import logging
import sys
from pathlib import Path

error_log = str(Path.cwd() / "logs/errors.log")
info_log = str(Path.cwd() / "logs/info.log")

# Обработчик успешного выполнения команд
loggerinfo = logging.getLogger("info")
loggerinfo.setLevel(logging.INFO)

file_handler = logging.FileHandler(info_log, encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

loggerinfo.addHandler(file_handler)

info_console_handler = logging.StreamHandler(sys.stdout)
info_console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
loggerinfo.addHandler(info_console_handler)


# Обработчик ошибок выполнения команд
loggererror = logging.getLogger("error")
loggererror.setLevel(logging.ERROR)

file_handler = logging.FileHandler(error_log, encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

loggererror.addHandler(file_handler)

error_console_handler = logging.StreamHandler(sys.stderr)
error_console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
loggererror.addHandler(error_console_handler)
