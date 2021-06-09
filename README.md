# Reminder App
A Reminder App made with Python for Linux

## Why?

I wanted to solve my own problem of reminding myself to do basic stuff I need to do every hour or so that I forget cause of work so this App came into existence.

## How does it work?

- Reminders are stored in JSON file *Saved-Reminders.JSON* in a Human Readable format
- It uses `notify-send` command in Linux to send notifications of Specific reminder that matches the current time of the system
- Reminders are automatically sorted using **Heap Data Structure**

## How to use it for yourself?

- Update the *Saved-Reminders.json* according to your needs
- Execute the script using the following command while in the current directory (of the Reminder App)

```bash
nohub python3 app.py &
```

It will execute the script in the Background.

**Note:**
If you use nohup, and want to terminate the script, use `kill` or `pkill` command for terminating the execution.
