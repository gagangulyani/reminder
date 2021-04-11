from subprocess import run


COMMAND = "notify-send"


def send_notification(app_name="Reminder 🐍", message="Blink", time=5000):
    attrs = {
        "a": app_name,
        "t": time,
        "u": "normal"
    }

    format_quotes = "-{0} \"{1}\""
    format_without_quotes = "-{0} {1}"

    final_command = " ".join(
        (format_quotes.format(attr, val) if type(val) != int else format_without_quotes.format(attr, val) for attr, val in attrs.items()))

    final_command = f"{COMMAND} {final_command} \"{message}\""
    print(final_command)
    run(final_command, shell=True, check=True)


if __name__ == "__main__":
    send_notification()
