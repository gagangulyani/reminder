from subprocess import run
from datetime import datetime, timedelta
from time import sleep
from types import FunctionType
from json import load
from pathlib import Path
from sys import argv, exit as sys_exit
from typing import Union, Any, Callable

REMINDER_FILE_PATH: Path = Path(__file__).parent / "reminders.json"


def is_finished(task: str) -> bool:
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


def clean_dt(datetime_obj: datetime) -> datetime:
    """This function returns the stripped version of datetime object
    with seconds and microseconds set to 0

    Args:
        datetime_obj (datetime): datetime object that needs to be stripped

    Returns:
        datetime: stripped datetime object
    """
    return datetime_obj.replace(microsecond=0)


def execute_at_time(custom_datetime: datetime, func: Callable, *args: list[Any], **kwargs: dict) -> bool:
    """This function calls the given function at a specific time (matching current time with time in future)

    Args:
        custom_datetime (datetime): [description]
        func (FunctionType): [description]

    Returns:
        bool: [description]
    """
    while True:
        if clean_dt(datetime.now()) == clean_dt(custom_datetime):
            return func(*args, **kwargs)
        else:
            sleep(1)


def get_path_to_reminders() -> None:
    """This function gets the path to reminders.json file consisting of reminders that need to be
    reminded to the user at their respective time and updates the global REMINDER_FILE_PATH object.

    Returns:
        None
    """
    global REMINDER_FILE_PATH

    if len(argv) not in [1, 2]:
        print("[ERROR] Invalid Number of Command Line Arguments!")
        sys_exit(1)

    elif len(argv) == 1 and REMINDER_FILE_PATH.exists():
        print("Reminders file found!")

    elif len(argv) == 2 and Path(argv[1]).exists():
        REMINDER_FILE_PATH = Path(argv[1])
        print("Reminders file found!")

    else:
        print("[ERROR] Can't find the JSON file containing the reminders...")
        sys_exit(2)


def dict_to_reminder(reminder: dict) -> dict:
    """This function converts the time in given reminder dictionary
    into Python datetime/timedelta objects for working with them.

    Args:
        reminder (dict): Dictionary containing timestamp in string format
    Returns:
        dict: consisting of reminder dictionary
    """
    temp: Union[str, datetime]
    if temp := reminder.get("gap", False):
        if "00:" in temp:
            if temp.count(":") == 2:
                temp = datetime.strptime(temp.removeprefix("00:"), "%M:%S")

            else:
                temp = datetime.strptime(temp.removeprefix("00:"), "%M")

        elif temp.count(":") == 2:
            temp = datetime.strptime(temp, "%I:%M:%S")

        else:
            temp = datetime.strptime(temp, "%I:%M")

        reminder["gap"] = timedelta(hours=temp.hour,
                                    minutes=temp.minute,
                                    seconds=temp.second)

    elif temp := reminder.get("time", False):
        temp = datetime.strptime(temp, "%H:%M %p")
        reminder["time"] = datetime.now().replace(hour=temp.hour,
                                                  minute=temp.minute,
                                                  second=0,
                                                  microsecond=0)

    return reminder


def start_app() -> None:
    """This function controls the reminders using defined functions in this module
    for working with them and displaying them to the users periodically.

    Returns:
        None: It doesn't return anything lol
    """

    # TODO:
    #   1. Display Reminders respective of their time
    #   2. Update the JSON file for disabling the reminder if repeat is disabled

    list_of_reminders: list[dict] = []

    with open(REMINDER_FILE_PATH, "r") as reminder_file:
        reminders = load(reminder_file)

        for reminder in reminders:
            list_of_reminders.append(dict_to_reminder(reminder))

    print(list_of_reminders)


if __name__ == "__main__":
    # print(execute_at_time(datetime.now() +
    #                       timedelta(seconds=5), is_finished, "Does it Work?"))
    start_app()
