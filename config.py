import threading

VERSION = "1.0"
CREATOR = "Created by Hunoka07"
PROJECT_NAME = "Dark Sashimi"

REQUIRED_PYTHON_VERSION = (3, 8)
DEFAULT_THREADS = {
    "Guerilla": 75,
    "Saturation": 400,
    "Annihilation": 2000
}
PROXY_TIMEOUT = 6

PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/proxiesmaster/Free-HTTPS-proxies/main/proxy.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Lists/main/free.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/main/http.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt"
]
USER_AGENT_URL = "https://raw.githubusercontent.com/elliotwutingfeng/latest-user-agents/main/latest-user-agents.json"
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

