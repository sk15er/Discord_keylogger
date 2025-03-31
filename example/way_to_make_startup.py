import os
import sys
import winreg

def add_to_startup_registry():
    try:
        # Path to your exe file (current executable)
        exe_path = sys.executable
        app_name = "MyApp"  # Change this to your app's name

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

# Call the function on first run
if __name__ == "__main__":
    add_to_startup_registry()
