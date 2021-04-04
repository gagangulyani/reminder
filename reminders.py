from notifier import send_notification
from time import sleep

while True:
    send_notification("Look Away from Screen and Blink 10 Times", 10000)
    sleep(20 * 60)
