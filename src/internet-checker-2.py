import logging
import os
import platform
import subprocess
import time
import tkinter as tk
from threading import Thread
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


class InternetCheckerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Internet Status Checker")
        self.status_label = tk.Label(
            root, text="Checking internet status...", font=("Arial", 14)
        )
        self.status_label.pack(pady=20)

        self.host = "google.com"
        self.was_down = False
        self.ping_results: List[bool] = [True] * 5  # Initialize with 5 successful pings

        self.running = True
        self.check_thread = Thread(target=self.check_internet_status)
        self.check_thread.start()

    def check_internet_status(self) -> None:
        """
        Continuously check the internet status and update the GUI.
        """
        try:
            while self.running:
                # Perform a ping and update the ping results
                self.ping_results.pop(0)  # Remove the oldest result
                self.ping_results.append(ping(self.host))  # Add the newest result

                # Count the number of failed pings in the last 5 results
                failed_pings = self.ping_results.count(False)

                if failed_pings >= 4:
                    if not self.was_down:
                        notify("Internet Down", "Internet is disconnected or slow 😞")
                        playsound("sound/beep.mp3")
                    self.update_status("Internet is disconnected or slow 😞")
                    self.was_down = True
                else:
                    if self.was_down:
                        notify("Internet Restored", "Internet is restored 😊")

                        playsound("sound/restore.mp3")
                        self.update_status("Internet is restored 😊")
                        self.was_down = False
                    else:
                        self.update_status("Internet is active 😊")

                time.sleep(0.5)  # Add seconds of interval
        except KeyboardInterrupt:
            print("[!] Exiting...")

    def update_status(self, status: str) -> None:
        """
        Update the status label in the GUI.

        Args:
            status (str): The status message to display.
        """
        self.status_label.config(text=status)

    def stop(self):
        """
        Stop the internet checking thread.
        """
        self.running = False
        self.check_thread.join()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x100")
    app = InternetCheckerApp(root)
    root.protocol(
        "WM_DELETE_WINDOW", app.stop
    )  # Ensure the thread stops on window close
    root.mainloop()
