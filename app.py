from reminders import Reminder
from os import getpid
from heapq import heapify, heappush, heappop, heappushpop
from terminal_output import display_table


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

        # print(terminal_size)
        ratios = [2, 2, 5, 2, 1]

        display_table(rows=list(self.reminders),
                      header=column_names, ratios=ratios)


if __name__ == "__main__":
    app = App()

    for _ in range(11):
        app.add_reminder(Reminder(
            message="Look away from screen, and blink 10 times!" f"{_}",
            time=60 * (_ + 1)
        ))

    app.display_reminders()
