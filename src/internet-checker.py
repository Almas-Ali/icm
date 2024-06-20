import logging
import os
import platform
import subprocess
import time
from typing import List

from notifypy import Notify # notify-py

# Disable playsound warning
logging.disable(logging.WARNING)
from playsound import playsound # playsound


def notify(title: str, message: str) -> None:
    """
    Send a desktop notification.

    Args:
        title (str): The title of the notification.
        message (str): The message of the notification.
    """
    notification = Notify()
    notification.title = title
    notification.message = message
    notification.send()


def ping(host: str) -> bool:
    """
    Ping the specified host to check for connectivity.

    Args:
        host (str): The host to ping.

    Returns:
        bool: True if the host is reachable, False otherwise.
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    with open(os.devnull, "w") as devnull:
        result = subprocess.run(command, stdout=devnull, stderr=devnull)
    return result.returncode == 0


def check_internet_status() -> None:
    """
    Continuously check the internet status and notify the user when the
    internet is disconnected or restored.
    """
    host = "google.com"
    was_down = False
    ping_results: List[bool] = [True] * 5  # Initialize with 5 successful pings

    try:
        while True:
            # Perform a ping and update the ping results
            ping_results.pop(0)  # Remove the oldest result
            ping_results.append(ping(host))  # Add the newest result

            # Count the number of failed pings in the last 5 results
            failed_pings = ping_results.count(False)

            if failed_pings >= 4:
                if not was_down:
                    notify("Internet Down", "Internet is disconnected or slow 😞")
                playsound("sound/beep.mp3")
                print("Internet is disconnected or slow 😞", end="\r")
                was_down = True
            else:
                if was_down:
                    notify("Internet Restored", "Internet is restored 😊")
                    playsound("sound/restore.mp3")
                    print("Internet is restored 😊                ", end="\r")
                    was_down = False

                print("Internet is active 😊                 ", end="\r")

            time.sleep(0.1)  # Add seconds of interval
    except KeyboardInterrupt:
        print("[!] Exiting...")


if __name__ == "__main__":
    check_internet_status()
