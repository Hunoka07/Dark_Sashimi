import threading

VERSION = "1.0"
CREATOR = "Created by TLG"
REQUIRED_PYTHON_VERSION = (3, 7)

DEFAULT_THREADS = {
    "Stealth": 50,
    "Overload": 250,
    "Blitz": 1000
}

PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/proxy4free/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt"
]

USER_AGENT_URL = "https://raw.githubusercontent.com/datasets/top-user-agents/main/user-agents.json"
PROXY_VALIDATION_TARGET = "http://httpbin.org/get"
PROXY_TIMEOUT = 8

attack_stats = {
    "requests_sent": 0,
    "sockets_opened": 0,
    "bytes_sent": 0,
    "errors": 0,
    "start_time": 0,
    "active_threads": 0,
    "threat_intelligence": "Initializing system..."
}

stop_event = threading.Event()
proxies = []
user_agents = []
