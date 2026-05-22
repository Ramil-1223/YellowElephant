import subprocess
from config.get_env import custom_env

def get_run():
    return subprocess.run

def get_env():
    return custom_env