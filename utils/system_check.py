import sys
import requests
from rich.console import Console

import config

console = Console()

def check_python_version():
    if sys.version_info < config.REQUIRED_PYTHON_VERSION:
        console.print(f"[bold red]FATAL: Outdated Python version. Requires Python {'.'.join(map(str, config.REQUIRED_PYTHON_VERSION))} or newer.[/bold red]")
        sys.exit(1)

def fetch_user_agents():
    with console.status("[bold cyan]Fetching User-Agent profiles...[/bold cyan]"):
        try:
            ua_res = requests.get(config.USER_AGENT_URL, timeout=10)
            ua_res.raise_for_status()
            config.user_agents = [item['user_agent'] for item in ua_res.json()]
            console.log(f"[green]Acquired {len(config.user_agents)} User-Agent profiles.[/green]")
        except Exception as e:
            console.log(f"[yellow]Could not fetch User-Agent list: {e}. Using default.[/yellow]")
            if not config.user_agents:
                config.user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"]

def initial_environment_check():
    check_python_version()
    fetch_user_agents()
