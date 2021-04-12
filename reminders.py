from notifier import send_notification
from time import sleep
from datetime import timedelta
from custom_decorators import validate_type


APP_NAME = "Reminder 🐍"


class Reminder:
    def __init__(self, message, time, title=None, life=5000):
        self.title = APP_NAME if title is None else title
        self.message = message
        self.time = timedelta(seconds=time)
        self.life = life

    def notify(self):
        send_notification(app_name=self.title,
                          message=self.message, time=self.life)

    def __repr__(self):
        return(f"Reminder(title = {self.title!a} "
               f", message = {self.message!a} "
               f", time = {self.time} "
               f", life = {self.life})"
               )

    def to_dict(self):
        return {
            "title": self.title,
            "message": self.message,
            "time": str(self.time),
            "life": f"{str(self.life / 1000)}s"
        }

    @validate_type
    def __lt__(self, other_reminder):
        return self.time < other_reminder.time

    @validate_type
    def __gt__(self, other_reminder):
        return self.time > other_reminder.time

    @validate_type
    def __le__(self, other_reminder):
        return self.time <= other_reminder.time

    @validate_type
    def __ge__(self, other_reminder):
        return self.time >= other_reminder.time

    @validate_type
    def __eq__(self, other_reminder):
        return self.time == other_reminder.time

    @validate_type
    def __ne__(self, other_reminder):
        return self.time == other_reminder.time


if __name__ == "__main__":

    for _ in range(10):
        Reminder("Hello, World!", 10).notify()
        sleep(10)
