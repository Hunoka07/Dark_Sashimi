import time
from urllib.parse import urlparse
import cloudscraper
from rich.table import Table

from utils.display import console

class TargetAnalytics:
    def __init__(self, target_url):
        self.url = target_url
        self.domain = urlparse(self.url).netloc
        self.results = {}
        self.scraper = cloudscraper.create_scraper()

    def run_analysis(self):
        with console.status(f"[bold magenta]Analyzing target: {self.domain}...[/bold magenta]"):
            self.results['Target'] = self.domain
            self.check_reachability_and_headers()
        
        if self.results.get("Status") == "Unreachable":
            self.display_report()
            return None
            
        self.measure_latency()
        self.display_report()
        return self.results

    def check_reachability_and_headers(self):
        try:
            response = self.scraper.get(self.url, timeout=10)
            self.results['Status'] = f"{response.status_code} {response.reason}"
            headers = {k.lower(): v for k, v in response.headers.items()}
            server = headers.get('server', 'N/A').lower()

            if 'cloudflare' in server: self.results['Protection'] = "Cloudflare"
            elif 'sucuri' in server: self.results['Protection'] = "Sucuri CloudProxy"
            elif any(k in headers for k in ['x-amz-cf-id', 'x-aws-waf-token']): self.results['Protection'] = "AWS WAF/CloudFront"
            else: self.results['Protection'] = "Unknown/None"

            self.results['Server'] = server.capitalize()
            self.results['Content-Type'] = headers.get('content-type', 'N/A')
            
        except requests.exceptions.RequestException as e:
            self.results['Status'] = "Unreachable"
            self.results['Error'] = str(type(e).__name__)

    def measure_latency(self):
        timings = []
        with console.status(f"[bold magenta]Measuring network latency...[/bold magenta]"):
            for _ in range(3):
                try:
                    start = time.time()
                    self.scraper.head(self.url, timeout=5)
                    end = time.time()
                    timings.append((end - start) * 1000)
                except requests.exceptions.RequestException:
                    timings.append(float('inf'))
        
        if all(t == float('inf') for t in timings):
            self.results['Avg. Latency'] = "Timeout"
        else:
            valid_timings = [t for t in timings if t != float('inf')]
            avg_latency = sum(valid_timings) / len(valid_timings)
            self.results['Avg. Latency'] = f"{avg_latency:.2f} ms"

    def display_report(self):
        table = Table(title=f"Target Analysis: {self.domain}", style="magenta", title_style="bold magenta", border_style="blue")
        table.add_column("Parameter", style="cyan", no_wrap=True)
        table.add_column("Finding", style="white")
        for key, value in self.results.items():
            table.add_row(key, str(value))
        console.print(table)
