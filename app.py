from reminders import Reminder
from os import getpid
from heapq import heapify, heappush, heappop, heappushpop
from string import Template


class App:
    def __init__(self):
        self.reminders = []
        heapify(self.reminders)
        print("App initialized! 🔥")

    def add_reminder(self, reminder=None):
        reminder = self.create_reminder() if reminder is None else reminder
        heappush(self.reminders, reminder)
        # print("Reminder added to the list! ✅")

    def create_reminder(self):
        title = input("What should be the title for reminder? "
                      "[default = \"Reminder 🐍\"]\n▶ ")
        message = input("What is the Message for Reminder?\n▶ ")
        time = int(input("How much time should it take?\n▶ "))
        life = int(input("For how long it should stay on screen? "
                         "[default = \"5000 (ms)\"]\n▶ "))

        title = None if title == "" else title
        life = 5000 if life == "" else life

        return Reminder(title=title, message=message,
                        life=life, time=time)

    def display_reminders(self):
        print("🔽 Current Reminders (from high to low priority) 🔽\n")
        column_names = ['Priority', 'Title', 'Message', 'Time', 'Life']

        template = (
            "{priority:-^10}{title:-^14}"
            "{message:-^15}{time:-^10}{life:-^10}")

        header = template.format(**(
            {k.lower(): val for k, val in zip(column_names, column_names)}
        ))

        # Header
        print("=" * len(header))

        print(header)

        print("=" * len(header))

        print()

        template = template.replace("-", " ")

        for i, reminder in enumerate(list(self.reminders)):
            print(template.format(
                priority=i + 1,
                title=reminder.title,
                message=reminder.message,
                time=str(reminder.time),
                life=reminder.life
            ))

        print("=" * len(header))


if __name__ == "__main__":
    app = App()

    for _ in range(11):
        app.add_reminder(Reminder(
            message="Hello, World!" f"{_}",
            time=60 * (_ + 1)
        ))

    app.display_reminders()
