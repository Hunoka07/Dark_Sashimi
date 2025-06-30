import threading

VERSION = "X"
CREATOR = "Created by Hunoka07"
PROJECT_NAME = "Dark Sashimi"

REQUIRED_PYTHON_VERSION = (3, 8)
DEFAULT_THREADS = {
    "Guerilla": 80,
    "Saturation": 500,
    "Annihilation": 2500
}
PROXY_TIMEOUT = 6

PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/VolkanSah/Auto-Proxy-Fetcher/main/proxies.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
]
USER_AGENT_URL = "https://raw.githubusercontent.com/brands/data/main/data/user-agents.json"
PROXY_VALIDATION_TARGETS = ["https://httpbin.org/get", "https://api.ipify.org?format=json"]

attack_stats = {
    "requests_sent": 0, "bytes_sent": 0, "http_ok": 0,
    "http_error": 0, "connect_error": 0, "timeout_error": 0,
    "start_time": 0, "active_threads": 0, "proxy_total": 0,
    "proxy_validated": 0, "threat_intelligence": "Hệ thống sẵn sàng..."
}
stop_event = threading.Event()
proxies = []
user_agents = []

