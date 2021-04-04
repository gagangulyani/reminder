from subprocess import check_output

APP_NAME = "Reminder"
COMMAND = "notify-send"


def send_notification(message="Blink", time=5000):
    attrs = {
        "a": APP_NAME,
        "t": time,
        "u": "normal"
    }

    final_command = " ".join(
        (f"-{attr} {val}" for attr, val in attrs.items()))

    final_command = f"{COMMAND} {final_command} \"{message}\""

    print(check_output(final_command, shell=True))


if __name__ == "__main__":
    send_notification()
