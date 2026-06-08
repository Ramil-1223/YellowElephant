import questionary
from questionary import prompt
from data.choices import ChoiceList, ChoiceCluster, FormatBackup, DirBackup, Confirm
from data.interface_text import *
from prompt_toolkit.styles import Style


custom_style = Style([
    ("question", "fg:#ff0000 bold"),
    ("answer", "fg:#4688f1 bold"),
    ("pointer", "fg:#336791 bold"),
    ("highlighted", "fg:#336791 bold"),
    ("text", "fg:#ffff00 bold"),
])

def exit_from_cli():
    questionary.press_any_key_to_continue(
        exit, style=custom_style
    ).ask()

def wait_for_continue():
    result = questionary.press_any_key_to_continue(
        return_to_main_menu, style=custom_style
    ).ask()
    if result is None:
        questionary.print(keyboard_interrupt, style="bold red")


def ask_main_menu():
    questions = [
        {
            "type": "select",
            "name": "action",
            "message": "Выберите действие:",
            "choices": [c.value for c in ChoiceList],
            "qmark": "",
            "instruction": " ",
        }
    ]
    result = prompt(questions, style=custom_style)
    return result["action"] if result else None


def ask_create_base():
    questions = [
        {
            "type": "select",
            "name": "cluster",
            "message": choice_cluster,
            "choices": [c.value for c in ChoiceCluster],
            "qmark": "",
            "instruction": " ",
        },
        {
            "type": "text",
            "name": "create_dbname",
            "message": input_name_base,
            "qmark": "",
            "validate": lambda text: (
                True if 1 <= len(text) <= 20 else "Допустимая длина от 1 до 20"
            ),
        },
        {
            "type": "text",
            "name": "description",
            "message": input_description,
            "qmark": "",
            "validate": lambda text: (
                True if 1 <= len(text) <= 30 else "Допустимая длина от 1 до 30"
            ),
        },
    ]
    result = prompt(questions, style=custom_style)
    return result if result else None


def ask_drop_base_pg():
    questions = [
        {
            "type": "text",
            "name": "drop_dbname",
            "message": input_name_base,
            "qmark": "",
            "validate": lambda text: (
                True if 1 <= len(text) <= 20 else "Допустимая длина от 1 до 20"
            ),
        },
        {
            "type": "select",
            "name": "accept_drop",
            "message": accept_drop,
            "choices": [c.value for c in Confirm],
            "qmark": "",
            "instruction": " ",
        },
    ]
    result = prompt(questions, style=custom_style)
    return result if result else None


def ask_drop_base_1c():
    questions = [
        {
            "type": "select",
            "name": "cluster",
            "message": choice_cluster,
            "choices": [c.value for c in ChoiceCluster],
            "qmark": "",
            "instruction": " ",
        },
        {
            "type": "text",
            "name": "drop_dbname",
            "message": input_name_base,
            "qmark": "",
            "validate": lambda text: (
                True if 1 <= len(text) <= 20 else "Допустимая длина от 1 до 20"
            ),
        },
        {
            "type": "select",
            "name": "accept_drop",
            "message": accept_drop,
            "choices": [c.value for c in Confirm],
            "qmark": "",
            "instruction": " ",
        },
    ]
    result = prompt(questions, style=custom_style)
    return result if result else None


def ask_backup_base():
    questions = [
        {
            "type": "select",
            "name": "backup_format",
            "message": choice_format_backup,
            "choices": [c.value for c in FormatBackup],
            "qmark": "",
            "instruction": " ",
        },
        {
            "type": "select",
            "name": "backup_dir",
            "message": choice_dir_backup,
            "choices": [c.value for c in DirBackup],
            "qmark": "",
            "instruction": " ",
        },
        {
            "type": "text",
            "name": "backup_dbname",
            "message": input_name_base,
            "qmark": "",
            "instruction": " ",
            "validate": lambda text: (
                True if 1 <= len(text) <= 20 else "Допустимая длина от 1 до 20"
            ),
        },
    ]
    result = prompt(questions, style=custom_style)
    return result if result else None


def ask_cluster_for_list():
    questions = [
        {
            "type": "select",
            "name": "cluster",
            "message": choice_cluster,
            "choices": [c.value for c in ChoiceCluster],
            "qmark": "",
            "instruction": " ",
        }
    ]
    result = prompt(questions, style=custom_style)
    return result["cluster"] if result else None