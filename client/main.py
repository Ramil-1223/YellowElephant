import questionary
import httpx
from data.choices import ChoiceList, ChoiceCluster, FormatBackup, DirBackup, Confirm
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from data.http_paths import *
from data.interface_text import *
from style.questionary_style import custom_style

console = Console()

def main_menu():
    
    main = questionary.select(
        "Выберите действие:",
        choices = list(ChoiceList),
        qmark = "",
        instruction = " ",
        style = custom_style
    ).ask()
    return main

def main_route():
    while True:
        console.clear()
        table = Table()
        answers = main_menu()

        match answers:
            case ChoiceList.CREATE_BASE:
                create = questionary.form(
                    cluster = questionary.select(choice_cluster, choices = list(ChoiceCluster), style = custom_style, qmark = "", instruction = " "),
                    create_dbname = questionary.text(input_name_base, style = custom_style, qmark = "", validate = lambda text: True if len(text) > 0 and len(text) <= 20 else "Допустимая длина от 1 до 20"),
                    description = questionary.text(input_description, style = custom_style, qmark = "", validate = lambda text: True if len(text) > 0 and len(text) <= 30 else "Допустимая длина от 1 до 30")
                ).ask()
                if 'description' not in create:
                    questionary.print(keyboard_interrupt, style="bold red")
                    questionary.press_any_key_to_continue(return_to_main_menu).ask()
                    continue
                params = {'description': create['description'], 'port': 'None', 'cluster_id': create['cluster'], 'dbname': create['create_dbname']}
                with Progress(SpinnerColumn(), TextColumn("[bold cyan]{task.description}"), transient = True) as progress:
                    progress.add_task(description = "Выполняется создание базы...", total = None)
                    response = httpx.post(http_create, json = params, timeout = 20.0)
                questionary.print(response.text, style = "bold yellow")
                questionary.press_any_key_to_continue(return_to_main_menu, style = custom_style).ask()
            case ChoiceList.DROP_BASE_PG:
                drop = questionary.form(
                    drop_dbname = questionary.text(input_name_base, style = custom_style, qmark = "", validate = lambda text: True if len(text) > 0 and len(text) <= 20 else "Допустимая длина от 1 до 20"),
                    accept_drop = questionary.select(message = accept_drop, choices = list(Confirm), style = custom_style, qmark = "", instruction = " ")
                ).ask()
                if 'accept_drop' not in drop:
                    questionary.print(keyboard_interrupt, style = "bold red")
                    questionary.press_any_key_to_continue(return_to_main_menu, style = custom_style).ask()
                    continue
                elif drop['accept_drop'] == "Y":
                    params = drop['drop_dbname']
                    with Progress(SpinnerColumn(), TextColumn("[bold cyan]{task.description}"), transient = True) as progress:
                        progress.add_task(description = "Выполняется удаление базы из СУБД postgres...", total = None)
                        response = httpx.post(http_drop, content = params, timeout = 20.0)
                    questionary.print(response.text, style = "bold yellow")
                    questionary.press_any_key_to_continue(return_to_main_menu, style = custom_style).ask()
                else:
                    questionary.print(cancel_drop, style = "bold red")
                    questionary.press_any_key_to_continue(return_to_main_menu, style = custom_style).ask()   
                    continue
            case ChoiceList.DROP_BASE_1C:
                drop = questionary.form(
                    cluster = questionary.select(choice_cluster, choices = list(ChoiceCluster), style = custom_style, qmark = "", instruction = " "),
                    drop_dbname = questionary.text(input_name_base, style = custom_style, qmark = "", validate = lambda text: True if len(text) > 0 and len(text) <= 20 else "Допустимая длина от 1 до 20"),
                    accept_drop = questionary.select(message = accept_drop, choices = list(Confirm), style = custom_style, qmark = "", instruction = " ")
                ).ask()
                if 'accept_drop' not in drop:
                    questionary.print(keyboard_interrupt, style = "bold red")
                    questionary.press_any_key_to_continue(return_to_main_menu, style = custom_style).ask()
                    continue
                elif drop['accept_drop'] == "Y":
                    params = {'cluster': drop['cluster'], 'dbname': drop['drop_dbname']}                
                    with Progress(SpinnerColumn(), TextColumn("[bold cyan]{task.description}"), transient = True) as progress:
                        progress.add_task(description = "Выполняется удаление базы из кластера 1С...", total = None)
                        response = httpx.post(http_drop1C, json = params, timeout = 20.0)
                    questionary.print(response.text, style = "bold yellow")
                    questionary.press_any_key_to_continue(return_to_main_menu, style = custom_style).ask()
                else:
                    questionary.print(cancel_drop, style = "bold red")
                    questionary.press_any_key_to_continue(return_to_main_menu, style = custom_style).ask()   
                    continue
            case ChoiceList.BACKUP_BASE:
                backup = questionary.form(
                    backup_format = questionary.select(choice_format_backup, choices = list(FormatBackup), style = custom_style, qmark = "", instruction = " "),
                    backup_dir = questionary.select(choice_dir_backup, choices = list(DirBackup), style = custom_style, qmark = "", instruction = " "),
                    backup_dbname = questionary.text(input_name_base, style = custom_style, qmark = "", instruction = " ", validate = lambda text: True if len(text) > 0 and len(text) <= 20 else "Допустимая длина от 1 до 20")
                ).ask()
                if not backup or 'backup_dbname' not in backup:
                    questionary.print(keyboard_interrupt, style = "bold red")
                    questionary.press_any_key_to_continue(return_to_main_menu, style = custom_style).ask()
                    continue
                params = {'backup_format': backup['backup_format'], 'backup_dir': backup['backup_dir'], 'dbname': backup['backup_dbname']}
                with Progress(SpinnerColumn(), TextColumn("[bold cyan]{task.description}"), transient = True) as progress:
                    progress.add_task(description = "Выполняется резервное копирование...", total = None)
                    response = httpx.post(http_backup, json = params, timeout = None)
                questionary.print(response.text, style = "bold yellow")
                questionary.press_any_key_to_continue(return_to_main_menu, style = custom_style).ask()
            case ChoiceList.LS_BASE:
                cluster = questionary.select(choice_cluster, choices = list(ChoiceCluster), style = custom_style, qmark = "", instruction = " ").ask()
                response = httpx.post(http_list, json = cluster, timeout = 10.0)
                table.add_column(f"Список баз в кластере {cluster}", header_style = "#ff0000")
                table.add_row(response.text, style = "bold yellow")
                console.print(table)
                questionary.press_any_key_to_continue(return_to_main_menu, style = custom_style).ask()
            case ChoiceList.EXIT:
                break
            case _:
                questionary.print(keyboard_interrupt2, style = "bold yellow")
                break


if __name__ == "__main__":
    main_route()