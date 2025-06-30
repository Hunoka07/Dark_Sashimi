import sys
import requests
from rich.console import Console

import config

console = Console()

def check_python_version():
    if sys.version_info < config.REQUIRED_PYTHON_VERSION:
        console.print(f"[bold red]LỖI: Phiên bản Python quá cũ. Yêu cầu Python {'.'.join(map(str, config.REQUIRED_PYTHON_VERSION))} hoặc mới hơn.[/bold red]")
        sys.exit(1)

def fetch_user_agents():
    with console.status("[bold sky_blue2]Đang tải danh sách User-Agent...[/bold sky_blue2]"):
        try:
            ua_res = requests.get(config.USER_AGENT_URL, timeout=10)
            ua_res.raise_for_status()
            
            # This specific source nests the list under the "user_agents" key
            ua_data = ua_res.json()
            if "user_agents" in ua_data and isinstance(ua_data["user_agents"], dict):
                config.user_agents = [ua for category in ua_data["user_agents"].values() for ua in category]
            else: # Fallback for simple list format
                config.user_agents = ua_data

            console.log(f"[green]Tải thành công {len(config.user_agents)} định danh trình duyệt.[/green]")
        except Exception as e:
            console.log(f"[yellow]Cảnh báo: Không thể tải User-Agent: {e}. Sử dụng định danh mặc định.[/yellow]")
            if not config.user_agents:
                config.user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"]

def initial_environment_check():
    check_python_version()
    fetch_user_agents()

