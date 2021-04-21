from notifier import send_notification
from datetime import timedelta, datetime
from custom_decorators import validate_type


APP_NAME = "Reminder 🐍"


class Reminder:
    def __init__(self, message, time, title=None, life=5000):
        self.title = APP_NAME if title is None else title
        self.message = message
        self.time = timedelta(seconds=time)
        self.datetime = None
        self.life = life

    def add_ctime(self):
        self.datetime = (datetime.now() + self.time).replace(microsecond=0)
        return self

    def notify(self):
        send_notification(app_name=self.title,
                          message=self.message, time=self.life)

    def __repr__(self):
        return(f"Reminder(title={self.title!a}"
               f", message={self.message!a}"
               f", time={self.time}"
               f", datetime={self.datetime}"
               f", life={self.life})"
               )

    def to_dict(self):
        return {
            "title": self.title,
            "message": self.message,
            "time": self.time,
            "life": self.life / 1000,
            "datetime": self.datetime
        }

    def to_str_dict(self):
        temp = self.to_dict()
        temp["time"] = str(self.time)
        temp["life"] = f"{temp['life']}s"
        temp.pop("datetime")
        return temp

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
