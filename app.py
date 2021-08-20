from datetime import datetime, timedelta
from time import sleep
from json import load, dump
from sys import exit as sys_exit
from pathlib import Path
from helpers import (get_path_to_reminders, ask, notify)

REMINDER_FILE_PATH: Path = get_path_to_reminders()


def clean_dt(datetime_obj: datetime) -> datetime:
    """This function returns the stripped version of datetime object
    with microseconds set to 0

    Args:
        datetime_obj (datetime): datetime object that needs to be stripped

    Returns:
        datetime: stripped datetime object
    """
    return datetime_obj.replace(microsecond=0)


def dict_to_reminder(reminder: dict) -> dict:
    """This function converts the time in given reminder dictionary
    into Python datetime/timedelta objects for working with them.

    Args:
        reminder (dict): Dictionary containing timestamp in string format
    Returns:
        dict: consisting of reminder dictionary
    """
    gap = reminder.get("gap", None)
    time_ = reminder.get("time", None)

    if gap == None and time_ == None:
        print("[ERROR] Unable to find either of Gap or Time for the Reminder")
        sys_exit(4)

    if gap:
        if "00:" in gap:
            if gap.count(":") == 2:
                gap = datetime.strptime(gap.removeprefix("00:"), "%M:%S")

            else:
                gap = datetime.strptime(gap.removeprefix("00:"), "%M")

        elif gap.count(":") == 2:
            gap = datetime.strptime(gap, "%I:%M:%S")

        else:
            gap = datetime.strptime(gap, "%I:%M")

        reminder["gap"] = timedelta(hours=gap.hour,
                                    minutes=gap.minute,
                                    seconds=gap.second)

        reminder["time"] = datetime.now() + reminder["gap"]
        reminder["has_gap"] = True

    elif time_:
        try:
            time_ = datetime.strptime(time_, "%I:%M:%S %p")
        except ValueError:
            time_ = datetime.strptime(time_, "%I:%M %p")

        reminder["time"] = datetime.now().replace(hour=time_.hour,
                                                  minute=time_.minute,
                                                  second=time_.second)
        reminder["has_gap"] = False

    return reminder


def display_reminder(reminder: dict) -> bool:
    """This function displays reminder and returns boolean value
    indicating if reminder was successfully displayed.

    Returns
        bool: True, if reminder was successfully displayed, else False
    """
    time_: datetime = reminder["time"]
    msg: str = reminder["message"]

    if reminder.get("type") not in ["question", "notify"]:
        print("[ERROR] Invalid Reminder Type!")
        sys_exit(3)

    if clean_dt(datetime.now()) == clean_dt(time_):
        if reminder.get("type", None) == "question":
            return ask(msg)
        return notify(msg)

    return False


def is_in_future(reminder: dict) -> bool:
    """This function checks if the given reminder is in the future by checking the datetime

    Args:
        reminder (dict): [description]

    Returns:
        bool: [description]
    """

    future: datetime = datetime.now() + timedelta(seconds=10)

    return reminder.get("time", future) > datetime.now() or reminder.get("gap", False)


def get_reminders(raw=False) -> dict:
    """This function returns reminders from the JSON file containing reminders

    Returns:
        dict: Reminders
    """
    reminders: dict = {}
    temp: dict

    with open(REMINDER_FILE_PATH, "r") as reminder_file:
        if raw:
            return load(reminder_file)

        for reminder in load(reminder_file):
            temp = dict_to_reminder(reminder)
            if temp.get("enabled", False) and is_in_future(reminder):
                add_reminder_to_dict(reminders, temp)
            elif temp.get("enabled") == None:
                print(f"[ERROR] a reminder has no attribute \"enabled\"!")
                sys_exit(3)

        return reminders


def update_reminder_file(updated_reminder: dict, toggle: bool = False) -> None:
    """This function updates the reminder's "enabled" attribute used for enabling
    and disabling it, in the JSON file

    Args:
        updated_reminder (dict): Reminder

    Returns:
         bool: True if reminder has been updated else False
    """
    reminders: dict = get_reminders(raw=True)
    found: bool = False

    for reminder in reminders:
        if reminder["message"] == updated_reminder["message"]:
            if toggle:
                reminder["enabled"] = not updated_reminder["enabled"]
            else:
                reminder["enabled"] = updated_reminder["enabled"]
            found = True

    with open(REMINDER_FILE_PATH, "w") as reminder_file:
        dump(reminders, reminder_file, indent=4)

    if not found:
        raise OSError("Reminder file not Found!")


def add_reminder_to_dict(list_of_reminders: dict, reminder: dict) -> None:
    """This function adds reminder dict into list_of_reminders dict with key as reminder's time

    Args:
        list_of_reminders (dict): Dict of Reminders
        reminder (dict): dict containing info about the reminder
    """
    reminder["time"] = reminder["time"].replace(microsecond=0)

    if reminder["time"] in list_of_reminders:
        list_of_reminders[reminder["time"]].append(reminder)
    else:
        list_of_reminders[reminder["time"]] = [reminder]


def seconds_until_next_reminder(list_of_reminders: dict) -> int:
    ith_reminder: datetime
    smallest_reminder: int = 9999999999999999999999

    for ith_reminder in list_of_reminders:
        difference = (ith_reminder - clean_dt(datetime.now())).seconds
        if difference < smallest_reminder:
            smallest_reminder = difference

    return smallest_reminder


def start_app():
    """This function controls the reminders using defined functions in this module
    for working with them and displaying them to the users periodically.
    """

    list_of_reminders: dict = get_reminders()
    while list_of_reminders:
        ctime = clean_dt(datetime.now())
        if list_of_reminders.get(ctime):
            reminders = list_of_reminders.pop(ctime)
            for reminder in reminders:
                if display_reminder(reminder):
                    if reminder["repeat"] and reminder["has_gap"]:
                        reminder["time"] += reminder["gap"]
                        add_reminder_to_dict(list_of_reminders, reminder)
                    else:
                        update_reminder_file(reminder, toggle=True)
                else:
                    add_reminder_to_dict(list_of_reminders, reminder)
        else:
            seconds: int = seconds_until_next_reminder(list_of_reminders)
            sleep(seconds)


if __name__ == "__main__":
    start_app()
