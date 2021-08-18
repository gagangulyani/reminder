from subprocess import run
from pathlib import Path
from sys import argv, exit as sys_exit


def ask(task: str) -> bool:
    """This function returns the return value of zenity
    command's question that user responds to

    Args:
        task (str): task that needs to be completed

    Returns:
        bool: True if User Selected Yes (Task has been completed) else False
    """
    command = f"zenity --question --title \"Reminder\" --text \"{task}\" 2>/dev/null --no-wrap"
    output = run(command, shell=True)
    return not bool(output.returncode)


def notify(task: str) -> bool:
    """This function notifies the user with the message in the reminder

    Returns:
         bool: True if command was successfully executed else False
    """
    output = run(f"notify-send -a \"Reminder\" \"{task}\"", shell=True)
    return not bool(output.returncode)


def get_path_to_reminders() -> Path:
    """This function gets the path to reminders.json file consisting of reminders that need to be
    reminded to the user at their respective time and updates the global REMINDER_FILE_PATH object.

    Returns:
        Path: Path object containing JSON file's path
    """

    temp_path: Path = Path(__file__).parent / "reminders.json"

    if len(argv) not in [1, 2]:
        print("[ERROR] Invalid Number of Command Line Arguments!")
        sys_exit(1)

    elif len(argv) == 1 and temp_path.exists():
        # print("Reminders file found!")
        return temp_path

    elif len(argv) == 2 and (path := Path(argv[1])).exists():
        # print("Reminders file found!")
        return path

    else:
        print("[ERROR] Can't find the JSON file containing the reminders...")
        sys_exit(2)
