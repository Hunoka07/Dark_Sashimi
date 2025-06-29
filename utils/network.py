import requests
import random
import asyncio
import aiohttp
from rich.console import Console

import config

console = Console()

def fetch_proxies():
    all_proxies = set()
    for url in config.PROXY_SOURCES:
        try:
            res = requests.get(url, timeout=5)
            res.raise_for_status()
            for proxy in res.text.splitlines():
                if proxy.strip():
                    all_proxies.add(proxy.strip())
        except requests.exceptions.RequestException:
            console.log(f"[yellow]Warning: Failed to fetch proxy list from {url}[/yellow]")
    return list(all_proxies)

async def validate_proxy(session, proxy):
    try:
        proxy_url = f"http://{proxy}"
        async with session.get(config.PROXY_VALIDATION_TARGET, proxy=proxy_url, timeout=config.PROXY_TIMEOUT) as response:
            if response.status == 200:
                return proxy
    except (aiohttp.ClientError, asyncio.TimeoutError):
        pass
    return None

async def run_validation(proxies_to_check):
    validated = []
    async with aiohttp.ClientSession() as session:
        tasks = [validate_proxy(session, proxy) for proxy in proxies_to_check]
        results = await asyncio.gather(*tasks)
        validated = [res for res in results if res is not None]
    return validated

def get_validated_proxies():
    with console.status("[bold cyan]Acquiring and validating proxies...[/bold cyan]", spinner="dots"):
        raw_proxies = fetch_proxies()
        if not raw_proxies:
            console.log("[bold red]No proxies could be fetched. Attack may be ineffective.[/bold red]")
            return

        try:
            validated_list = asyncio.run(run_validation(raw_proxies))
            config.proxies = validated_list
            console.log(f"[bold green]Acquired {len(config.proxies)} validated proxies.[/bold green]")
        except Exception as e:
            console.log(f"[bold red]An error occurred during async proxy validation: {e}. Using raw list.[/bold red]")
            config.proxies = raw_proxies

def get_random_proxy():
    if config.proxies:
        return {'http': f"http://{random.choice(config.proxies)}", 'https': f"http://{random.choice(config.proxies)}"}
    return None

def get_random_user_agent():
    if config.user_agents:
        return random.choice(config.user_agents)
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

