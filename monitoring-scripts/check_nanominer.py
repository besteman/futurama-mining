from subprocess import check_output
from os import system
import typing


def process_exists(process_name: str) -> bool:
    programs: str = str(check_output('tasklist'))

    if process_name in programs:
        return True
    else:
        return False


def restart_system(program: str) -> None:
    is_program_running: bool = process_exists(program)

    if is_program_running:
        print(f"{program} is Running")
        return
    else:
        print(f"{program} is not Running\n")
        print("Restarting")
        os.system("shutdown /r /t 1")


restart_system('nanominer')