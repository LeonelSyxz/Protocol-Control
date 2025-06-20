import time
import threading
import subprocess
from database import db
import os

class HLSController:
    def __init__(self):
        self.running = False
        self.thread = None
        self.adb_path = os.path.join("utils", "adb.exe")

    def start_loop(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._loop)
            self.thread.start()

    def stop_loop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def _loop(self):
        while self.running:
            loop_interval = db.get_loop_interval()
            tvs = db.get_tvs()
            
            direction_keyevents = {
                "up": "KEYCODE_CHANNEL_UP",
                "down": "KEYCODE_CHANNEL_DOWN"
            }

            direction_roku = {
                "up": "Up",
                "down": "Down"
            }

            for tv in tvs:
                tv_id, name, ip, os_type, direction, status = tv
                if not status:
                    continue

                try:
                    direction = direction.lower()
                    if os_type == "Google TV":
                        connect_cmd = f"{self.adb_path} connect {ip}"
                        subprocess.run(connect_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                        key_event = direction_keyevents.get(direction, "KEYCODE_CHANNEL_UP")
                        command = f"{self.adb_path} -s {ip} shell input keyevent {key_event}"
                        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        print(f"[{name}] Google TV channel changed ({direction}).")

                    elif os_type == "Roku OS":
                        roku_direction = direction_roku.get(direction, "Up")
                        command = f"curl -s -X POST http://{ip}:8060/keypress/{roku_direction}"
                        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        print(f"[{name}] Roku channel changed ({direction}).")

                except Exception as e:
                    print(f"Error with {name} ({ip}): {e}")

            time.sleep(loop_interval)
