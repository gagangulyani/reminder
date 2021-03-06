from notifier import send_notification
from datetime import timedelta, datetime as dt
from custom_decorators import validate_type
from uuid import uuid4

APP_NAME = "Reminder 🐍"


class Reminder:
    def __init__(self, message, time, title=None, life=5, datetime=None,
                 is_enabled=False, repeat=False, id=None):
        self.title = APP_NAME if title is None else title
        self.message = message
        self.time = timedelta(seconds=time)
        self.datetime = datetime if datetime is not None else dt.now().replace(microsecond=0)
        self.life = life
        self.is_enabled = is_enabled
        self.repeat = repeat
        self.id = str(uuid4())[::5] if id == None else id

    def add_ctime(self):
        self.datetime = (dt.now() + self.time).replace(microsecond=0)
        return self

    def notify(self, verbose=False):
        send_notification(app_name=self.title,
                          message=self.message, time=self.life * 1000,
                          verbose=verbose)

    def __repr__(self):
        return(f"Reminder(title={self.title!a}"
               f", message={self.message!a}"
               f", time={self.time.__repr__()}"
               f", datetime={self.datetime.__repr__()}"
               f", life={self.life.__repr__()}"
               f", is_enabled={self.is_enabled}"
               f", repeat={self.repeat})"
               f", id={self.id!a})"
               )

    def to_dict(self, to_str=False, ignore_datetime=False):
        temp = {
            "title": self.title,
            "message": self.message,
            "time": self.time,
            "life": self.life,
            "datetime": self.datetime,
            "is_enabled": self.is_enabled,
            "repeat": self.repeat,
            "id": self.id
        }
        if ignore_datetime:
            temp.pop("datetime")

        return {key: str(value) for key, value in temp.items()} if to_str else temp

    @staticmethod
    def to_time(time_str):

        if type(time_str) == int:
            return time_str

        if time_str in [None, "None"]:
            return None

        #  For Life Attr
        if time_str.endswith("s"):
            return int(time_str.removesuffix("s"))

        if time_str.endswith("m"):
            return int(time_str.removesuffix("m")) * 60

        if time_str.isdigit():
            return int(time_str)

        # For Time Attr
        if "-" not in time_str:

            days = 0

            if "day" in time_str:
                days, _, time_str = time_str.split()

            time_str = time_str.split(":")

            hours, minutes, seconds = [
                int(i) for i in time_str]

            days = int(days) * 24 * 60 * 60
            hours *= 60 * 60
            minutes *= 60

            seconds += days+hours+minutes
            return seconds

        # For Date Attr
        return dt.fromisoformat(time_str)

    @staticmethod
    def to_bool(bool_str):
        return True if bool_str.lower() == "true" else False

    @staticmethod
    def from_dict(dict_):
        return Reminder(
            title=dict_.get("title", APP_NAME),
            message=dict_.get("message"),
            time=Reminder.to_time(dict_.get("time")),
            life=Reminder.to_time(dict_.get("life")),
            datetime=Reminder.to_time(dict_.get("datetime", None)),
            is_enabled=Reminder.to_bool(dict_.get("is_enabled")),
            repeat=Reminder.to_bool(dict_.get("repeat", "False")),
            id=dict_.get("id", None)
        )

    @validate_type
    def __lt__(self, other_reminder):
        return self.datetime < other_reminder.datetime

    @validate_type
    def __gt__(self, other_reminder):
        return self.datetime > other_reminder.datetime

    @validate_type
    def __le__(self, other_reminder):
        return self.datetime <= other_reminder.datetime

    @validate_type
    def __ge__(self, other_reminder):
        return self.datetime >= other_reminder.datetime

    @validate_type
    def __eq__(self, other_reminder):
        return self.to_dict() == other_reminder.to_dict()

    @validate_type
    def __ne__(self, other_reminder):
        return self.to_dict() != other_reminder.to_dict()


if __name__ == "__main__":
    from time import sleep
    for _ in range(10):
        Reminder("Hello, World!", 10).notify()
        sleep(10)
