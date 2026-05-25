from enum import StrEnum


class ChoiceList(StrEnum):
    CREATE_BASE = "1. Создать базу"
    DROP_BASE_PG = "2. Удалить базу из СУБД postgres"
    DROP_BASE_1C = "3. Удалить базу из кластера 1С"
    BACKUP_BASE = "4. Сделать резервную копию базы"
    LS_BASE = "5. Вывести список баз в кластере 1С"
    EXIT = "6. Выйти"


class ChoiceCluster(StrEnum):
    TEST = "test"
    DEMO = "demo"


class FormatBackup(StrEnum):
    CUSTOM = "custom"
    DIRECTORY = "directory"
    TAR = "tar"
    PLAIN = "plain-text"


class DirBackup(StrEnum):
    TEST = "/backup_base/backup_test"
    DEMO = "/backup_base/backup_demo"


class Confirm(StrEnum):
    YES = "Y"
    NO = "N"
