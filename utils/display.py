# -*- coding: utf-8 -*-
import threading
import time
import os
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.columns import Columns

import config

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_main_banner():
    banner = """
██████╗  █████╗ ██████╗ ██╗  ██╗    ███████╗  █████╗  ███████╗ ██╗  ██╗ ██╗ ███╗   ██╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██╔════╝ ██╔══██╗██╔════╝ ██║  ██║ ██║ ████╗  ██║
██║  ██║███████║██████╔╝█████╔╝     ███████╗ ███████║███████╗ ███████║ ██║ ██╔██╗ ██║
██║  ██║██╔══██║██╔══██╗██╔═██╗     ╚════██║ ██╔══██║╚════██║ ██╔══██║ ██║ ██║╚██╗██║
██████╔╝██║  ██║██║  ██║██║  ██╗    ███████║ ██║  ██║███████║ ██║  ██║ ██║ ██║ ╚████║
╚═════╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝ ╚═╝  ╚═╝╚══════╝ ╚═╝  ╚═╝ ╚═╝ ╚═╝  ╚═══╝                                                                     
    """
    console.print(Text(banner, style="bold #8A2BE2"), justify="center")
    console.print(Text(f"{config.PROJECT_NAME} v{config.VERSION} - {config.CREATOR}", style="bold cyan"), justify="center")
    console.rule("[bold #FFD700]Hệ thống Kiểm tra Hiệu năng Thế hệ mới[/bold #FFD700]")

def get_proxy_panel():
    total = config.attack_stats["proxy_total"]
    validated = config.attack_stats["proxy_validated"]
    return Panel(
        Text(f"Tổng cộng: [bold green]{total}[/bold green]\nHoạt động: [bold cyan]{validated}[/bold cyan]", justify="center"),
        title="[b]Trạng thái Proxy[/b]", border_style="yellow"
    )

def get_error_panel():
    conn_err = config.attack_stats['connect_error']
    timeout_err = config.attack_stats['timeout_error']
    http_err = config.attack_stats['http_error']
    return Panel(
        Text(f"Kết nối: [red]{conn_err:,}[/red]\nTimeout: [red]{timeout_err:,}[/red]\nHTTP: [red]{http_err:,}[/red]", justify="left"),
        title="[b]Thống kê Lỗi[/b]", border_style="red"
    )

def get_attack_stats_panel():
    elapsed = max(time.time() - config.attack_stats["start_time"], 1)
    rps = config.attack_stats["requests_sent"] / elapsed
    
    total_ok = config.attack_stats["http_ok"]
    total_err = config.attack_stats["http_error"] + config.attack_stats["connect_error"] + config.attack_stats["timeout_error"]
    total_req = total_ok + total_err
    success_rate = (total_ok / total_req * 100) if total_req > 0 else 100

    data_sent = config.attack_stats["bytes_sent"]
    if data_sent > 1024**3: data_str = f"{data_sent / 1024**3:.2f} GB"
    elif data_sent > 1024**2: data_str = f"{data_sent / 1024**2:.2f} MB"
    else: data_str = f"{data_sent / 1024:.2f} KB"
    
    rate_str = f"{data_sent / elapsed / 1024**2:.2f} MB/s"

    table = Table(show_header=False, show_edge=False, box=None)
    table.add_column(style="cyan", justify="right")
    table.add_column(style="bold white", justify="left")
    table.add_row("RPS :", f" {rps:,.1f}")
    table.add_row("Tỉ lệ thành công :", f"[bold {'green' if success_rate > 70 else 'yellow' if success_rate > 30 else 'red'}]{success_rate:.1f}%[/bold]")
    table.add_row("Luồng hoạt động :", f" {config.attack_stats['active_threads']}")
    table.add_row("Băng thông :", f" {rate_str}")
    
    return Panel(table, title="[b]Hiệu suất Tấn công[/b]", border_style="green")

def update_threat_intelligence():
    total_req = config.attack_stats["requests_sent"] + config.attack_stats["sockets_opened"]
    if total_req < 30: return
    
    total_ok = config.attack_stats["http_ok"]
    total_err = config.attack_stats["http_error"] + config.attack_stats["connect_error"] + config.attack_stats["timeout_error"]
    
    if total_req > 0:
        err_rate = (total_err / total_req * 100)
        if err_rate > 95:
            config.attack_stats["threat_intelligence"] = "Tỉ lệ lỗi cực cao. Các proxy gần như bị vô hiệu hóa. Hãy tìm nguồn proxy mới hoặc dừng chiến dịch."
        elif err_rate > 70:
            config.attack_stats["threat_intelligence"] = "Hệ thống phòng thủ của mục tiêu đang hoạt động rất hiệu quả. Cân nhắc chuyển sang chế độ 'Du kích' để tránh bị phát hiện."
        elif total_ok > 200:
            config.attack_stats["threat_intelligence"] = "Tấn công đang diễn ra ổn định. Máy chủ mục tiêu đang chịu áp lực lớn. Tiếp tục duy trì!"

def run_dashboard_loop():
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=5),
        Layout(name="main"),
        Layout(name="footer", size=3),
    )
    layout["main"].split_row(
        Layout(name="left"),
        Layout(name="right", ratio=2),
    )
    layout["left"].split(
        Layout(name="proxy"),
        Layout(name="errors"),
    )

    layout["header"].update(Align.center(Text(f"{config.PROJECT_NAME}", style="bold #FFD700 on #8A2BE2"), vertical="middle"))
    layout["footer"].update(Align.center(Text("Nhấn [bold]CTRL+C[/bold] để kết thúc chiến dịch an toàn.", style="yellow"), vertical="middle"))
    
    with Live(layout, screen=True, redirect_stderr=False, vertical_overflow="visible", refresh_per_second=5) as live:
        while not config.stop_event.is_set():
            update_threat_intelligence()
            layout["right"].update(get_attack_stats_panel())
            layout["proxy"].update(get_proxy_panel())
            layout["errors"].update(get_error_panel())
            live.console.rule(f"[bold purple]{config.attack_stats['threat_intelligence']}[/bold purple]")
            time.sleep(1/5)

def launch_dashboard():
    dashboard_thread = threading.Thread(target=run_dashboard_loop, daemon=True)
    dashboard_thread.start()
    return dashboard_thread
