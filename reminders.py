from notifier import send_notification
from datetime import timedelta, datetime
from custom_decorators import validate_type


APP_NAME = "Reminder 🐍"


class Reminder:
    def __init__(self, message, time, title=None, life=5, datetime=None, is_enabled=False):
        self.title = APP_NAME if title is None else title
        self.message = message
        self.time = timedelta(seconds=time)
        self.datetime = datetime
        self.life = life
        self.is_enabled = is_enabled

    def add_ctime(self):
        self.datetime = (datetime.now() + self.time).replace(microsecond=0)
        return self

    def notify(self, verbose=False):
        send_notification(app_name=self.title,
                          message=self.message, time=self.life * 1000,
                          verbose=verbose)

    def __repr__(self):
        return(f"Reminder(title={self.title!a}"
               f", message={self.message!a}"
               f", time={self.time}"
               f", datetime={self.datetime}"
               f", life={self.life})"
               f", is_enabled={self.is_enabled}"
               )

    def to_dict(self, to_str=False):
        temp = {
            "title": self.title,
            "message": self.message,
            "time": self.time,
            "life": self.life,
            "datetime": self.datetime,
            "is_enabled": self.is_enabled
        }

        return {key: str(value) for key, value in temp.items()} if to_str else temp

    @staticmethod
    def to_time(time_str):

        if time_str == None:
            return time_str
            
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
                days, temp, time_str = time_str.split()

            time_str = time_str.split(":")

            hours, minutes, seconds = [
                int(i) for i in time_str]

            days = int(days) * 24 * 60 * 60
            hours *= 60 * 60
            minutes *= 60

            seconds += days+hours+minutes
            return seconds

        # For Date Attr
        return datetime.fromisoformat(time_str)

    @staticmethod
    def to_bool(bool_str):
        return True if bool_str.lower() == "true" else False

    @staticmethod
    def from_dict(dict_):
        return Reminder(
            title=dict_.get("title"),
            message=dict_.get("message"),
            time=Reminder.to_time(dict_.get("time")),
            life=Reminder.to_time(dict_.get("life")),
            datetime=Reminder.to_time(dict_.get("datetime", None)),
            is_enabled=Reminder.to_bool(dict_.get("is_enabled"))
        )

    @validate_type
    def __lt__(self, other_reminder):
        if self.datetime != None:
            return self.datetime < other_reminder.datetime
        return self.time < other_reminder.time

    @validate_type
    def __gt__(self, other_reminder):
        if self.datetime != None:
            return self.datetime > other_reminder.datetime
        return self.time > other_reminder.time

    @validate_type
    def __le__(self, other_reminder):
        if self.datetime != None:
            return self.datetime <= other_reminder.datetime
        return self.time <= other_reminder.time

    @validate_type
    def __ge__(self, other_reminder):
        if self.datetime != None:
            return self.datetime >= other_reminder.datetime
        return self.time >= other_reminder.time

    @validate_type
    def __eq__(self, other_reminder):
        if self.datetime != None:
            return self.datetime == other_reminder.datetime
        return self.time == other_reminder.time

    @validate_type
    def __ne__(self, other_reminder):
        if self.datetime != None:
            return self.datetime != other_reminder.datetime
        return self.time != other_reminder.time


if __name__ == "__main__":
    from time import sleep
    for _ in range(10):
        Reminder("Hello, World!", 10).notify()
        sleep(10)
