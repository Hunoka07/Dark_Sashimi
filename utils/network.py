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
                res = requests.get(url, timeout=5)
                res.raise_for_status()
                for proxy in res.text.splitlines():
                    if proxy.strip():
                        self.raw_proxies.add(proxy.strip())
            except requests.exceptions.RequestException:
                console.log(f"[yellow]Cảnh báo: Không thể lấy proxy từ {url}[/yellow]")
        
        config.attack_stats["proxy_total"] = len(self.raw_proxies)

    async def validate_proxy(self, session, proxy):
        proxy_url = f"http://{proxy}"
        for target in config.PROXY_VALIDATION_TARGETS:
            try:
                async with session.get(target, proxy=proxy_url, timeout=config.PROXY_TIMEOUT) as response:
                    if response.status == 200:
                        return proxy
            except (aiohttp.ClientError, asyncio.TimeoutError):
                continue
        return None

    async def run_validation(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.validate_proxy(session, proxy) for proxy in self.raw_proxies]
            results = await asyncio.gather(*tasks)
            self.validated_proxies = [res for res in results if res is not None]
        
        config.proxies = self.validated_proxies
        config.attack_stats["proxy_validated"] = len(self.validated_proxies)

    def load_proxies(self):
        with console.status("[bold sky_blue2]Đang tổng hợp và kiểm tra proxy...[/bold sky_blue2]", spinner="dots12"):
            self.fetch_sources()
            if not self.raw_proxies:
                console.log("[bold red]Không thể lấy được bất kỳ proxy nào. Tấn công có thể không hiệu quả.[/bold red]")
                return

            try:
                asyncio.run(self.run_validation())
                console.log(f"[bold green]Kiểm tra hoàn tất: Thu được {len(config.proxies)} proxy hoạt động.[/bold green]")
            except Exception as e:
                console.log(f"[bold red]Lỗi khi kiểm tra proxy: {e}. Sử dụng danh sách thô.[/bold red]")
                config.proxies = list(self.raw_proxies)

def get_random_proxy():
    if config.proxies:
        return {'http': f"http://{random.choice(config.proxies)}", 'https': f"http://{random.choice(config.proxies)}"}
    return None

def get_random_user_agent():
    if config.user_agents:
        return random.choice(config.user_agents)
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

