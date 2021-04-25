from reminders import Reminder
from os import getpid
from os.path import exists
from heapq import heapify, heappush, heappop, heapreplace
from terminal_output import display_table
from datetime import datetime
from time import sleep
from pprint import pprint
from json import dump, load


# Save File name for the User
JSON_NAME = "Saved-Reminders.json"

# Current State file name (saves state each 500ms)
CURRENT_STATE_NAME = "current_state.json"

# Display Commands for Reminder
VERBOSE = False


class App:
    def __init__(self, reminders=None):
        self.reminders = [] if reminders == None else reminders
        heapify(self.reminders)
        print("App initialized! 🔥")

    def add_reminder(self, reminder=None):
        reminder = self.create_reminder() if reminder is None else reminder
        heappush(self.reminders, reminder)
        # print("Reminder added to the list! ✅")

    def create_reminder(self):
        # TODO: Add more inputs according to attributes of Reminder Class
        title = input("What should be the title for reminder? "
                      "[default = \"Reminder 🐍\"]\n▶ ")
        message = input("What is the Message for Reminder?\n▶ ")
        time = int(input("How much time should it take (in minutes)?\n▶ "))
        life = input("For how long it should stay on screen? "
                     "[default = \"5 (seconds)\"]\n▶ ")

        title = None if title == "" else title
        life = 5 if life == "" else Reminder.to_time(life)

        time = Reminder.to_time(time)  # Convert Minutes into Seconds

        return Reminder(title=title, message=message,
                        life=life, time=time)

    def display_reminders(self):
        if len(self.reminders) == 0:
            print("⚠ No Reminders Found❗")
            return
        print("🔽 Current Reminders (from HIGH to LOW Priority) 🔽\n")
        column_names = [key.capitalize()
                        for key in self.reminders[0].to_dict(to_str=True)]

        # Custom Ratio (optional)
        ratios = [15, 30]
        display_table(rows=sorted(self.reminders),
                      header=column_names, ratios=ratios)

    def generate_reminders(self, all, resume):
        if len(self.reminders) == 0 or resume == True:
            self.load_reminders(resume)

        if not all:
            self.reminders = [reminder.add_ctime()
                              for reminder in self.reminders if reminder.is_enabled]
        else:
            self.reminders = [reminder.add_ctime()
                              for reminder in self.reminders]
        heapify(self.reminders)

    def start(self, all=False, resume=False):

        self.generate_reminders(all, resume)

        app.display_reminders()

        while len(self.reminders) != 0:
            if self.reminders[0].datetime == datetime.now().replace(microsecond=0):
                self.reminders[0].notify(verbose=VERBOSE)
                if self.reminders[0].repeat == True:
                    heapreplace(self.reminders, self.reminders[0].add_ctime())
                else:
                    self.reminders[0].is_enabled = False
                    App.update_reminder(self.reminders[0])
                    heappop(self.reminders)

            elif self.reminders[0].datetime < datetime.now().replace(microsecond=0):
                print(f"Reminder with ID {self.reminders[0]!a} Expired!")
                if self.reminders[0].repeat == True:
                    print("Re-Added the Reminder with Updated Timings")
                    heapreplace(self.reminders, self.reminders[0].add_ctime())

            else:
                self.save_reminders(current_state=True)
                sleep(0.5)

    def to_dict(self, to_str=False, current_state=False):
        return [reminder.to_dict(to_str=to_str, ignore_datetime=not current_state) for reminder in self.reminders]

    @staticmethod
    def update_reminder(current_reminder, resume=False, current_state=False):
        print(current_reminder)
        reminders = App.load_json(resume=resume)
        for index, reminder in enumerate(reminders):
            if reminder.id == current_reminder.id:
                current_reminder.datetime = None
                reminders[index] = current_reminder
                break

        App(reminders).save_reminders(current_state)

    def save_reminders(self, current_state=False):
        filename = JSON_NAME if current_state is False else CURRENT_STATE_NAME
        dump(self.to_dict(to_str=True), open(
            filename, "w"), indent=4)

    @staticmethod
    def load_json(resume=False):
        filename = JSON_NAME if resume == False else CURRENT_STATE_NAME
        if exists(filename):
            return load(open(filename, "r"),
                        object_hook=Reminder.from_dict)
        print("[ERROR] Saved Reminders Not Found!")
        return []

    def load_reminders(self, resume=False):
        self.reminders = App.load_json(resume)


if __name__ == "__main__":
    app = App()

    # Automatically Generate Reminders (Non-Random)
    set_reminder = False

    # Ignore Disabled Reminders
    all = False

    # Resume Reminders from Current State
    resume = False

    #  for Testing
    if set_reminder == True:

        reminders = [
            Reminder(
                message="Look Away for 5 Seconds",
                time=5,
                repeat=True,
                is_enabled=True
            ),
            Reminder(
                message="Look Away for 5 more Seconds!",
                time=5, repeat=False,
                is_enabled=True
            ),
            Reminder(
                message="Look Away for 10 Seconds",
                time=10,
                repeat=True, is_enabled=True
            ),
        ]

        for reminder in reminders:
            app.add_reminder(reminder)

        app.save_reminders()

    app.start(all=all, resume=resume)
