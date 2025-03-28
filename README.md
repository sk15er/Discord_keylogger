# Discord Keylogger

> **Educational Purpose Only**  
> This project is intended for educational demonstrations on cybersecurity. Unauthorized use without explicit consent is illegal and unethical.

# ![image_for_discord](https://github.com/user-attachments/assets/2040d3b8-c1e2-47d1-b116-bd3f5fb555ef)


## Overview

The Discord Keylogger is a Python-based tool that records user keystrokes and periodically sends them, along with screenshots, to a specified Discord channel via a webhook. This project serves as a demonstration of potential security vulnerabilities and underscores the importance of robust cybersecurity practices.

## Features

- **Keystroke Logging**: Captures all user keystrokes in real-time.
- **Periodic Data Transmission**: Sends logged keystrokes and screenshots to a Discord channel at regular intervals.
- **Screenshot Capture**:
- ![image](https://github.com/user-attachments/assets/10b60bd7-4d75-476e-af49-24f28ae7ff67)

- **Stealth Operation**: Runs silently in the background without user notification.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sk15er/Discord_keylogger.git
   cd Discord_keylogger
   ```

2. **Install Required Libraries**:
   Ensure you have Python installed on your system. Then, install the necessary Python packages:
   ```bash
   pip install pynput requests pyautogui
   ```

## Configuration

1. **Set Up a Discord Webhook**:
   - Create a Discord server and channel where you want to receive the logs.
   - In the channel settings, navigate to **Integrations** > **Webhooks** and create a new webhook.
   - Copy the webhook URL for later use.

2. **Configure the Script**:
   - Open `main.py` in a text editor.
   - Locate the line defining `webhook_url` and replace the placeholder with your actual Discord webhook URL:
     ```python
     webhook_url = "YOUR_DISCORD_WEBHOOK_URL"
     ```

## Usage

Run the script using Python:
```bash
python main.py
```
The script will start logging keystrokes and capturing screenshots, sending the data to your specified Discord channel at regular intervals.

## File Structure

- `main.py`: The primary script that initializes and runs the keylogger.
- `keylogger.py`: Contains the `KeyLogger` class, encapsulating the keylogging and data transmission functionalities.
- `images/`: Directory where captured screenshots are temporarily stored before being sent.

## Legal and Ethical Considerations

This tool is intended solely for educational purposes. Unauthorized use to monitor individuals without their explicit consent is illegal and unethical. Always ensure you have the necessary permissions before deploying this tool.

## Disclaimer

The authors are not responsible for any misuse of this tool. It is provided as-is for educational purposes, and users assume all responsibility for its use.

---
