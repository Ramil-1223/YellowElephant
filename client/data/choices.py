from enum import StrEnum

class ChoiceList(StrEnum):
    CREATE_BASE = "1. Создать базу"
    DROP_BASE = "2. Удалить базу"
    BACKUP_BASE = "3. Сделать резервную копию базы"
    LS_BASE = "4. Вывести список баз"
    EXIT = "5. Выйти"

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