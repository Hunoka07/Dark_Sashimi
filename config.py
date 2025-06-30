import threading

VERSION = "2.0"
CREATOR = "Created by Hunoka07"
PROJECT_NAME = "Dark Sashimi v2"

REQUIRED_PYTHON_VERSION = (3, 8)
DEFAULT_THREADS = {
    "Guerilla": 100,
    "Saturation": 500,
    "Annihilation": 3000
}
PROXY_TIMEOUT = 7

PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/tarampampam/proxy-daily/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt"
]

USER_AGENT_URL = "https://raw.githubusercontent.com/lorien/user-agent-list/master/user-agents.json"
PROXY_VALIDATION_TARGET = "https://httpbin.org/get"

attack_stats = {
    "requests_sent": 0, "bytes_sent": 0, "http_ok": 0,
    "http_error": 0, "connect_error": 0, "timeout_error": 0,
    "start_time": 0, "active_threads": 0, "proxy_total": 0,
    "proxy_validated": 0, "threat_intelligence": "Hệ thống sẵn sàng..."
}
stop_event = threading.Event()
proxies = []
user_agents = []
