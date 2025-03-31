# Key logger for discord
### [Github_page](https://sk15er.github.io/Discord_keylogger/)
##### ![image](https://github.com/user-attachments/assets/e2cca18c-0593-40bd-997e-0b15f9b868d3)


**Disclaimer:** _This project is intended for educational purposes only. Unauthorized use without explicit consent is illegal and unethical. Always ensure you have the necessary permissions before deploying this tool._

## Overview

The Discord Keylogger is a Python-based tool that records user keystrokes and periodically sends them, along with screenshots, to a specified Discord channel via a webhook. This project serves as a demonstration of potential security vulnerabilities and underscores the importance of robust cybersecurity practices.

## Features

-   **Keystroke Logging:** Captures all user keystrokes in real-time.
    
-   **Periodic Data Transmission:** Sends logged keystrokes and screenshots to a Discord channel at regular intervals.
    
-   **Screenshot Capture:** Periodically captures screenshots of the user's screen.
    
-   **Stealth Operation:** Runs silently in the background without user notification.
    

## Installation
To install this keylogger, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/sk15er/Discord_keylogger.git
    cd Discord_keylogger
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
## Configuration

1.  **Set Up a Discord Webhook:**
    
    -   Create a Discord server and channel where you want to receive the logs.
        
    -   In the channel settings, navigate to **Integrations > Webhooks** and create a new webhook.
        
    -   Copy the webhook URL for later use.
        
2.  **Configure the Script:**
    
    -   Open `main.py` in a text editor.
        
    -   Locate the line defining `webhook_url` and replace the placeholder with your actual Discord webhook URL:
        
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

-   [`main.py`](https://github.com/sk15er/Discord_keylogger/blob/main/main.py): The primary script that initializes and runs the keylogger.
    
-   [`keylogger.py`](https://github.com/sk15er/Discord_keylogger/blob/main/keylogger.py): Contains the `KeyLogger` class, encapsulating the keylogging and data transmission functionalities.
    
-   [`Auto_startup.py`](https://github.com/sk15er/Discord_keylogger/blob/main/Auto_startup.py): Script designed to add the keylogger to system startup for persistence.
    
-   [`main_new.py`](https://github.com/sk15er/Discord_keylogger/blob/main/main_new.py): An alternative main script with potentially updated or experimental features.
    
-   [`test_audio.exe`](https://github.com/sk15er/Discord_keylogger/blob/main/test_audio.exe): An executable file, possibly for testing audio-related functionalities.
    
-   [`images/`](https://github.com/sk15er/Discord_keylogger/tree/main/images): Directory where captured screenshots are temporarily stored before being sent.
    
-   [`example/`](https://github.com/sk15er/Discord_keylogger/tree/main/example): Contains example files demonstrating the tool's functionality.
    
-   [`explain/`](https://github.com/sk15er/Discord_keylogger/tree/main/explain): Directory possibly containing documentation or explanations related to the project.
    
-   [`test/`](https://github.com/sk15er/Discord_keylogger/tree/main/test): Contains test scripts and related files for testing purposes.
    

## Recent Changes

-   **Auto Image Deletion:** Implemented a feature to automatically delete images after they have been sent to the Discord channel to conserve disk space. [Release: auto_delete_the_images](https://github.com/sk15er/Discord_keylogger/releases/tag/auto_delete_the_images)

## Releases
Check out the [Releases](https://github.com/sk15er/Discord_keylogger/releases) page for the latest versions and updates.

    

## Contributors

-   [shushank kumar (sk15er)](https://github.com/sk15er) - Orignal other
    
-   [shushank (Sk16er)](https://github.com/Sk16er) - Contributor 
    

## Legal and Ethical Considerations

This tool is intended solely for educational purposes. Unauthorized use to monitor individuals without their explicit consent is illegal and unethical. Always ensure you have the necessary permissions before deploying this tool.

## How it Works
The keylogger captures keystrokes using a Python library and sends the captured data to a Discord channel using a Discord bot. The keylogger runs in the background and continuously monitors keystrokes, sending batches of keystrokes at regular intervals.
## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Disclaimer

The authors are not responsible for any misuse of this tool. It is provided as-is for educational purposes, and users assume all responsibility for its use.
---

Feel free to update any section according to your specific requirements or preferences. Once you're satisfied with the README, you can update it in your repository.
