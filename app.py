from reminders import Reminder
from os import getpid
from os.path import exists
from heapq import heapify, heappush, heappop, heapreplace
from terminal_output import display_table
from datetime import datetime
from time import sleep
from pprint import pprint
from json import dump, load

JSON_NAME = "Saved-Reminders.json"
CURRENT_STATE_NAME = "current_state.json"
VERBOSE = False


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
        life = input("For how long it should stay on screen? "
                     "[default = \"5 (seconds)\"]\n▶ ")

        title = None if title == "" else title
        life = 5 if life == "" else int(life)

        time = int(time * 60)  # Convert Minutes into Seconds

        return Reminder(title=title, message=message,
                        life=life, time=time)

    def display_reminders(self):
        if len(self.reminders) == 0:
            print("⚠ No Reminders Found❗")
            return
        print("🔽 Current Reminders (from HIGH to LOW Priority) 🔽\n")
        column_names = [key.capitalize()
                        for key in self.reminders[0].to_dict(to_str=True)]

        # print(terminal_size)
        ratios = [20, 37, 15, 10, 20, 13]
        display_table(rows=sorted(self.reminders),
                      header=column_names, ratios=ratios)

    def start(self, all=False, resume=False):

        if len(self.reminders) == 0 or resume == True:
            self.load_reminders(resume)

        if not all:
            self.reminders = [reminder.add_ctime()
                              for reminder in self.reminders if reminder.is_enabled]
        else:
            self.reminders = [reminder.add_ctime()
                              for reminder in self.reminders]

        heapify(self.reminders)

        while len(self.reminders) != 0:
            if self.reminders[0].datetime == datetime.now().replace(microsecond=0):
                self.reminders[0].notify(verbose=VERBOSE)
                heapreplace(self.reminders, self.reminders[0].add_ctime())
            else:
                self.save_reminders(current_state=True)
                sleep(0.5)

    def to_dict(self, to_str=False):
        return [reminder.to_dict(to_str=to_str) for reminder in self.reminders]

    def save_reminders(self, current_state=False):
        filename = JSON_NAME if current_state is False else CURRENT_STATE_NAME
        dump(self.to_dict(to_str=True), open(
            filename, "w"), indent=4)

    def load_reminders(self, resume=False):
        filename = JSON_NAME if resume == False else CURRENT_STATE_NAME
        if exists(filename):
            self.reminders = load(open(filename, "r"),
                                  object_hook=Reminder.from_dict)
        else:
            print("Error! Saved Reminders Not Found!")
            self.reminders = []


if __name__ == "__main__":
    app = App()

    set_reminder = False

    # Ignore Disabled Reminders
    all = False

    #  for Testing
    if set_reminder == True:

        reminders = [
            Reminder(
                message="Look Away for 5 Seconds",
                time=5
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

        app.save_reminders()

    app.start(all=all)
