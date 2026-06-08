import httpx
import questionary
from rich.console import Console
from data.http_paths import *
from data.interface_text import *
from data.choices import ChoiceList
from utils.rich_helpers import run_with_spinner, print_single_column_table
from prompt.questionary_prompt import (
    ask_main_menu,
    ask_create_base,
    ask_drop_base_pg,
    ask_drop_base_1c,
    ask_backup_base,
    ask_cluster_for_list,
    exit_from_cli,
    wait_for_continue
)

console = Console()


def main_route():
    while True:
        console.clear()
        answers = ask_main_menu()

        match answers:
            case ChoiceList.CREATE_BASE:
                result = ask_create_base()
                if result is None:
                    wait_for_continue()
                    continue
                params = {
                    "description": result["description"],
                    "port": "None",
                    "cluster_id": result["cluster"],
                    "dbname": result["create_dbname"],
                }
                response = run_with_spinner(
                    "Выполняется создание базы...",
                    httpx.post,
                    http_create,
                    json=params,
                    timeout=20.0,
                )
                questionary.print(response.text, style = "bold yellow")
                wait_for_continue()


            case ChoiceList.DROP_BASE_PG:
                result = ask_drop_base_pg()
                if result is None:
                    wait_for_continue()
                    continue
                if result["accept_drop"] == "Y":
                    response = run_with_spinner(
                        "Выполняется удаление базы из СУБД postgres...",
                        httpx.post,
                        http_drop,
                        content=result["drop_dbname"],
                        timeout=20.0,
                    )
                    questionary.print(response.text, style="bold yellow")
                else:
                    questionary.print(cancel_drop, style="bold red")
                wait_for_continue()

            case ChoiceList.DROP_BASE_1C:
                result = ask_drop_base_1c()
                if result is None:
                    wait_for_continue()
                    continue
                if result["accept_drop"] == "Y":
                    params = {"cluster": result["cluster"], "dbname": result["drop_dbname"]}
                    response = run_with_spinner(
                        "Выполняется удаление базы из кластера 1С...",
                        httpx.post,
                        http_drop1C,
                        json=params,
                        timeout=20.0,
                    )
                    questionary.print(response.text, style="bold yellow")
                else:
                    questionary.print(cancel_drop, style="bold red")
                wait_for_continue()

            case ChoiceList.BACKUP_BASE:
                result = ask_backup_base()
                if result is None:
                    wait_for_continue()
                    continue
                params = {
                    "backup_format": result["backup_format"],
                    "backup_dir": result["backup_dir"],
                    "dbname": result["backup_dbname"],
                }
                response = run_with_spinner(
                    "Выполняется резервное копирование...",
                    httpx.post,
                    http_backup,
                    json=params,
                    timeout=None,
                )
                questionary.print(response.text, style="bold yellow")
                wait_for_continue()

            case ChoiceList.LS_BASE:
                cluster = ask_cluster_for_list()
                if cluster is None:
                    wait_for_continue()
                    continue
                response = run_with_spinner(
                    "Получение списка баз...",
                    httpx.post,
                    http_list,
                    json=cluster,
                    timeout=10.0,
                )
                print_single_column_table(f"Список баз в кластере {cluster}", response.text)
                wait_for_continue()

            case ChoiceList.EXIT:
                break
            case _:
                exit_from_cli()
                break


if __name__ == "__main__":
    main_route()