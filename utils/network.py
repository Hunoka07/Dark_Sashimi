import requests
import random
import asyncio
import aiohttp
from rich.console import Console
import config

console = Console()

class ProxyManager:
    def __init__(self):
        self.raw_proxies = set()
        self.validated_proxies = []

    def fetch_sources(self):
        for url in config.PROXY_SOURCES:
            try:
                res = requests.get(url, timeout=7)
                res.raise_for_status()
                for proxy in res.text.splitlines():
                    proxy = proxy.strip()
                    if proxy and all(c not in proxy for c in [' ', '\t', '#']):
                        self.raw_proxies.add(proxy)
            except Exception as e:
                console.log(f"[yellow]Không thể lấy proxy từ {url}: {e}[/yellow]")
        config.attack_stats["proxy_total"] = len(self.raw_proxies)

    async def validate_proxy(self, session, proxy):
        validation_targets = [config.PROXY_VALIDATION_TARGET, "https://api.ipify.org/"]
        for target in validation_targets:
            try:
                async with session.get(target, proxy=f"http://{proxy}", timeout=config.PROXY_TIMEOUT) as response:
                    if response.status == 200:
                        return proxy
            except Exception:
                continue
        return None

    async def run_validation(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.validate_proxy(session, proxy) for proxy in self.raw_proxies]
            results = await asyncio.gather(*tasks)
            self.validated_proxies = [res for res in results if res]
        config.proxies = self.validated_proxies
        config.attack_stats["proxy_validated"] = len(self.validated_proxies)

    def load_proxies(self):
        with console.status("[bold cyan]Đang lấy & kiểm tra proxy...[/bold cyan]", spinner="dots12"):
            self.fetch_sources()
            if not self.raw_proxies:
                console.log("[bold red]Không lấy được proxy nào. Chuyển sang không proxy![/bold red]")
                config.proxies = []
                return
            try:
                asyncio.run(self.run_validation())
                if config.proxies:
                    console.log(f"[bold green]Đã có {len(config.proxies)} proxy hoạt động![/bold green]")
                else:
                    console.log("[yellow]Không proxy nào hoạt động, dùng danh sách thô.[/yellow]")
                    config.proxies = list(self.raw_proxies)
            except Exception as e:
                console.log(f"[red]Lỗi khi kiểm tra proxy: {e}. Dùng danh sách thô.[/red]")
                config.proxies = list(self.raw_proxies)

def fetch_user_agents():
    try:
        res = requests.get(config.USER_AGENT_URL, timeout=7)
        res.raise_for_status()
        user_agents = res.json()
        if isinstance(user_agents, list) and user_agents:
            config.user_agents = user_agents
            console.log(f"[green]Đã lấy {len(user_agents)} user-agent![/green]")
            return
    except Exception as e:
        console.log(f"[yellow]Không thể lấy user-agent online: {e}. Sẽ dùng mặc định.[/yellow]")
    config.user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    ]

def get_random_proxy():
    if config.proxies:
        proxy = random.choice(config.proxies)
        return {'http': f"http://{proxy}", 'https': f"http://{proxy}"}
    return None

def get_random_user_agent():
    if config.user_agents:
        return random.choice(config.user_agents)
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
