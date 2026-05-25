import subprocess
import re
from config.get_env import custom_env


def get_run():
    return subprocess.run


def get_env():
    return custom_env


def get_dict_pattern(list_base):
    pattern = (
        r"infobase\s*:\s*(?P<infobase>[a-f0-9-]{36})\s*\n"
        r"name\s*:\s*(?P<name>[^\s\n]+)\s*\n"
        r"(?:\s*\n\s*descr\s*:\s*.*)?"
    )

    matches = re.finditer(pattern, list_base.stdout, re.MULTILINE)
    infobases = [match.groupdict() for match in matches]
    dict_idbase = {item["name"]: item["infobase"] for item in infobases}
    return dict_idbase


def get_str_pattern(list_base):
    pattern = (
        r"infobase\s*:\s*(?P<infobase>[a-f0-9-]{36})\s*\n"
        r"name\s*:\s*(?P<name>[^\s\n]+)\s*\n"
        r"(?:\s*\n\s*descr\s*:\s*.*)?"
    )

    matches = re.finditer(pattern, list_base.stdout, re.MULTILINE)
    infobases = [match.groupdict() for match in matches]
    list_bases = [item["name"] for item in infobases]
    str_base = "\n".join(list_bases)
    return str_base
