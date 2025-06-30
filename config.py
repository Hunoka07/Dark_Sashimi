import threading

VERSION = "1.0"
CREATOR = "Created by Hunoka07"
PROJECT_NAME = "Tonu"

REQUIRED_PYTHON_VERSION = (3, 8)
DEFAULT_THREADS = {
    "Guerilla": 80,
    "Saturation": 500,
    "Annihilation": 2500
}

USER_AGENT_URL = "https://raw.githubusercontent.com/brands/data/main/data/user-agents.json"

ADAPTIVE_INITIAL_DELAY = 1.0
ADAPTIVE_RAMP_UP_FACTOR = 0.8
ADAPTIVE_BACK_OFF_FACTOR = 1.5
ADAPTIVE_MAX_DELAY = 5.0
ADAPTIVE_MIN_DELAY = 0.05
ADAPTIVE_ERROR_THRESHOLD = 30

attack_stats = {
    "requests_sent": 0, "bytes_sent": 0, "http_ok": 0,
    "http_error": 0, "connect_error": 0, "timeout_error": 0,
    "start_time": 0, "active_threads": 0,
    "threat_intelligence": "Hệ thống sẵn sàng..."
}

stop_event = threading.Event()
user_agents = []
adaptive_delay = threading.local()
adaptive_delay.value = ADAPTIVE_INITIAL_DELAY
