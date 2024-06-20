import logging
import os
import platform
import subprocess
import time
from threading import Thread
from typing import List

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from notifypy import Notify

# Disable playsound warning
logging.disable(logging.WARNING)
from playsound import playsound


class InternetCheckerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status_label = Label(text="Checking internet status...", font_size="20sp")
        self.host = "google.com"
        self.was_down = False
        self.ping_results: List[bool] = [True] * 5  # Initialize with 5 successful pings
        self.running = True

    def build(self):
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(self.status_label)
        return layout

    def notify(self, title: str, message: str) -> None:
        notification = Notify()
        notification.title = title
        notification.message = message
        notification.send()

    def ping(self, host: str) -> bool:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", host]
        with open(os.devnull, "w") as devnull:
            result = subprocess.run(command, stdout=devnull, stderr=devnull)
        return result.returncode == 0

    def check_internet_status(self):
        while self.running:
            self.ping_results.pop(0)  # Remove the oldest result
            self.ping_results.append(self.ping(self.host))  # Add the newest result
            failed_pings = self.ping_results.count(False)

            if failed_pings >= 4:
                if not self.was_down:
                    self.notify("Internet Down", "Internet is disconnected or slow 😞")
                playsound("sound/beep.mp3")
                status = "Internet is disconnected or slow 😞"
                self.was_down = True
            else:
                if self.was_down:
                    self.notify("Internet Restored", "Internet is restored 😊")
                    playsound("sound/restore.mp3")
                    self.was_down = False
                
                status = "Internet is active 😊"

            Clock.schedule_once(lambda dt: self.update_status(status), 0)
            time.sleep(0.5)

    def update_status(self, status: str):
        self.status_label.text = status

    def on_stop(self):
        self.running = False
        self.checker_thread.join()

    def on_start(self):
        self.checker_thread = Thread(target=self.check_internet_status)
        self.checker_thread.start()


if __name__ == "__main__":
    InternetCheckerApp().run()
