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
        self.response_obj = None

    def run_analysis(self):
        with console.status(f"[bold magenta]Đang do thám mục tiêu: {self.domain}...[/bold magenta]"):
            self.results['Mục tiêu'] = self.domain
            self.check_reachability_and_headers()
        
        if "[red]Không thể truy cập[/red]" in self.results.get("Trạng thái", ""):
            self.display_report()
            return None, None
            
        self.measure_latency()
        self.display_report()
        return self.results, self.response_obj

    def check_reachability_and_headers(self):
        try:
            self.response_obj = self.scraper.get(self.url, timeout=10)
            self.results['Trạng thái'] = f"[green]{self.response_obj.status_code} {self.response_obj.reason}[/green]"
            headers = {k.lower(): v for k, v in self.response_obj.headers.items()}
            self.results['Máy chủ'] = headers.get('server', 'Không rõ').lower()
            
        except Exception as e:
            self.results['Trạng thái'] = "[red]Không thể truy cập[/red]"
            self.results['Lỗi'] = str(type(e).__name__)

    def measure_latency(self):
        timings = []
        with console.status(f"[bold magenta]Đo lường độ trễ mạng...[/bold magenta]"):
            for _ in range(3):
                try:
                    start_time = time.perf_counter()
                    self.scraper.head(self.url, timeout=5)
                    end_time = time.perf_counter()
                    timings.append((end_time - start_time) * 1000)
                except Exception:
                    continue
        
        if not timings:
            self.results['Độ trễ TB'] = "[red]Timeout[/red]"
        else:
            avg_latency = sum(timings) / len(timings)
            self.results['Độ trễ TB'] = f"{avg_latency:.2f} ms"

    def display_report(self):
        table = Table(title=f"Báo cáo Do thám: {self.domain}", style="magenta", title_style="bold magenta", border_style="blue")
        table.add_column("Tham số", style="cyan", no_wrap=True)
        table.add_column("Kết quả", style="white")
        for key, value in self.results.items():
            table.add_row(key, str(value))
        console.print(table)

