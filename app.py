from reminders import Reminder
from os import getpid
from heapq import heapify, heappush, heappop, heapreplace
from terminal_output import display_table
from datetime import datetime
from time import sleep
from pprint import pprint


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
        time = int(input("How much time should it take (in minutes)?\n▶ "))
        life = int(input("For how long it should stay on screen? "
                         "[default = \"5000 (ms)\"]\n▶ "))

        title = None if title == "" else title
        life = 5000 if life == "" else life

        time = int(time * 60)  # Convert Minutes into Seconds

        return Reminder(title=title, message=message,
                        life=life, time=time)

    def display_reminders(self):
        if len(self.reminders) == 0:
            print("⚠ No Reminders Found❗")
            return
        print("🔽 Current Reminders (from HIGH to LOW Priority) 🔽\n")
        column_names = ['Title', 'Message', 'Time', 'Life']

        # print(terminal_size)
        ratios = [20, 50, 15, 15]
        display_table(rows=sorted(self.reminders),
                      header=column_names, ratios=ratios)

    def start(self):
        self.reminders = [reminder.add_ctime() for reminder in self.reminders]
        heapify(self.reminders)
        # TODO: Make this function work!
        # previous = None
        # while len(self.reminders) != 0:
        #     current_reminder = self.reminders[0]
        #     if hasattr(previous, "datetime") and previous.datetime == current_reminder.datetime - previous.time:
        #         self.display_reminders()
        #     current_reminder.notify()
        #     previous = current_reminder
        #     heapreplace(self.reminders, current_reminder.add_ctime())
        #     sleep(current_reminder.time.seconds)

if __name__ == "__main__":
    app = App()

    reminders = [
        Reminder(
            message="Look Away for 5 Seconds",
            time=5
        ),
         Reminder(
            message="Look Away for 15 Seconds",
            time=15
        ),
        Reminder(
            message="Look Away for 5 more Seconds!",
            time=5
        ),
        Reminder(
            message="Look Away for 10 Seconds",
            time=10
        ),
       
    ]

    for reminder in reminders:
        app.add_reminder(reminder)
    # for _ in range(11):
    #     app.add_reminder(Reminder(
    #         message=("Look away from screen, and "
    #                  "blink 10 times and don't forget to breathe!! "
    #                  f"{_}"),
    #         time=60 * (_ + 1),
    #     ))

    app.display_reminders()

    # print()

    # for i in range(6):
    #     print(f"Starting Reminder App in {5-i} Seconds...", end="\r")
    #     sleep(1)

    app.start()
