from subprocess import check_output
from os import system
import typing


def process_exists(process_name: str) -> bool:
    """Checks to see if a process exists or is running

    Args:
        process_name (str): Process/App to check if running

    Returns:
        bool: boolean base on if Process/App is running
    """
    programs: str = str(check_output('tasklist'))

    if process_name in programs:
        return True
    else:
        return False


def restart_system(program: str) -> None:
    """Will restart machine if program is not running

    Args:
        program (str): Process/App to check if running
    """
    is_program_running: bool = process_exists(program)

    if is_program_running:
        print(f"{program} is Running")
        return
    else:
        print(f"{program} is not Running\n")
        print("Restarting")
        system("shutdown /r /t 1")


restart_system('nanominer')