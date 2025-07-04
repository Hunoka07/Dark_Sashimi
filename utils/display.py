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
from rich.markup import escape

import config

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_main_banner():
    banner_text = Text.from_markup("""
████████╗ ██████╗ ███╗   ██╗██╗   ██╗
╚══██╔══╝██╔═══██╗████╗  ██║██║   ██║
   ██║   ██║   ██║██╔██╗ ██║██║   ██║
   ██║   ██║   ██║██║╚██╗██║██║   ██║
   ██║   ╚██████╔╝██║ ╚████║╚██████╔╝
   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ 
    """, style="bold #8A2BE2", justify="center")
    
    project_text = Text(f"{config.PROJECT_NAME} v{config.VERSION} - {config.CREATOR}", style="bold cyan", justify="center")
    
    console.print(banner_text)
    console.print(project_text)
    console.rule(f"[bold #FFD700]Hệ thống Trí tuệ Tác chiến v{config.VERSION}[/bold #FFD700]")

def display_ai_report(plan):
    report_text = Text(plan["summary_report"], justify="left")
    report_panel = Panel(
        report_text,
        title="[bold gold1]Báo cáo từ AI Trợ chiến[/bold gold1]",
        border_style="gold1",
        padding=(1, 2)
    )
    
    table = Table(show_header=False, box=None, padding=0)
    table.add_row(Text("Mức độ nguy hiểm:", style="cyan"), Text.from_markup(plan["threat_level"]))
    table.add_row(Text("Vector đề xuất:", style="cyan"), Text(plan['vector'], style="bold green"))
    table.add_row(Text("Cường độ đề xuất:", style="cyan"), Text(plan['mode'], style="bold green"))
    table.add_row(Text("Số luồng đề xuất:", style="cyan"), Text(str(plan['threads']), style="bold green"))
    
    console.print(report_panel)
    console.print(table)

def make_layout():
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="left_side", minimum_size=30),
        Layout(name="right_side", ratio=2),
    )
    layout["left_side"].split(Layout(name="proxy_info"), Layout(name="error_info"))
    layout["right_side"].split(Layout(name="attack_stats"), Layout(name="intel_report"))
    return layout

def run_dashboard_loop():
    layout = make_layout()
    layout["header"].update(Align.center(Text(f"{config.PROJECT_NAME} v{config.VERSION}", style="bold #FFD700 on #8A2BE2"), vertical="middle"))
    layout["footer"].update(Align.center(Text("Nhấn [bold]CTRL+C[/bold] để kết thúc chiến dịch an toàn.", style="yellow"), vertical="middle"))
    
    with Live(layout, screen=True, redirect_stderr=False, vertical_overflow="visible", refresh_per_second=5) as live:
        while not config.stop_event.is_set():
            proxy_panel = Panel(
                Text(f"Đã lấy: [bold green]{config.attack_stats['proxy_total']:,}[/bold green]\nHoạt động: [bold cyan]{config.attack_stats['proxy_validated']:,}[/bold cyan]", justify="center"), 
                title="[b]Proxy[/b]", 
                border_style="yellow"
            )
            error_panel = Panel(
                Text(f"Kết nối: [red]{config.attack_stats['connect_error']:,}[/red]\nTimeout: [red]{config.attack_stats['timeout_error']:,}[/red]\nHTTP: [red]{config.attack_stats['http_error']:,}[/red]", justify="left"), 
                title="[b]Lỗi[/b]", 
                border_style="red"
            )

            elapsed = max(time.time() - config.attack_stats.get("start_time", time.time()), 1)
            rps = config.attack_stats["requests_sent"] / elapsed
            total_ok = config.attack_stats["http_ok"]
            total_err = config.attack_stats["http_error"] + config.attack_stats["connect_error"] + config.attack_stats["timeout_error"]
            total_req = total_ok + total_err
            success_rate = (total_ok / total_req * 100) if total_req > 0 else 100
            
            success_rate_color = "green" if success_rate > 70 else "yellow" if success_rate > 30 else "red"
            success_rate_text = Text(f"{success_rate:.1f}%", style=f"bold {success_rate_color}")
            
            stats_table = Table(show_header=False, show_edge=False, box=None)
            stats_table.add_row(Text("RPS :", style="cyan", justify="right"), Text(f" {rps:,.1f}", style="bold white"))
            stats_table.add_row(Text("Thành công :", style="cyan", justify="right"), success_rate_text)
            stats_table.add_row(Text("Luồng :", style="cyan", justify="right"), Text(f" {config.attack_stats['active_threads']}", style="bold white"))

            main_panel = Panel(stats_table, title="[b]Hiệu suất Tấn công[/b]", border_style="green")
            
            update_threat_intelligence()
            intel_text = Text(config.attack_stats['threat_intelligence'])
            intel_panel = Panel(intel_text, title="[b]Tình báo Chiến thuật[/b]", border_style="magenta")

            layout["proxy_info"].update(proxy_panel)
            layout["error_info"].update(error_panel)
            layout["attack_stats"].update(main_panel)
            layout["intel_report"].update(intel_panel)

            time.sleep(1/5)

def launch_dashboard():
    dashboard_thread = threading.Thread(target=run_dashboard_loop, daemon=True)
    dashboard_thread.start()
    return dashboard_thread
    
def update_threat_intelligence():
    total_req = config.attack_stats["requests_sent"]
    if total_req < 50: 
        config.attack_stats["threat_intelligence"] = "Đang thu thập dữ liệu chiến trường..."
        return
    
    total_ok = config.attack_stats["http_ok"]
    total_err = config.attack_stats["http_error"] + config.attack_stats["connect_error"] + config.attack_stats["timeout_error"]
    
    if total_req > 0:
        err_rate = (total_err / total_req * 100)

        if not config.proxies:
            if err_rate > config.ADAPTIVE_ERROR_THRESHOLD and config.adaptive_delay.value < config.ADAPTIVE_MAX_DELAY:
                config.adaptive_delay.value *= config.ADAPTIVE_BACK_OFF_FACTOR
                config.attack_stats["threat_intelligence"] = "[AI]: Phát hiện kháng cự! Đang tự động giảm tốc độ để bảo vệ IP."
            elif err_rate < 10 and config.adaptive_delay.value > config.ADAPTIVE_MIN_DELAY:
                config.adaptive_delay.value *= config.ADAPTIVE_RAMP_UP_FACTOR
                config.attack_stats["threat_intelligence"] = "[AI]: Mục tiêu có vẻ ổn định. Đang từ từ tăng áp lực."
            else:
                config.attack_stats["threat_intelligence"] = "[AI]: Đang duy trì tốc độ tấn công thích ứng."
        else:
            if err_rate > 95:
                config.attack_stats["threat_intelligence"] = "Tỉ lệ lỗi cực cao. Proxy gần như bị vô hiệu hóa. Dừng lại và tìm nguồn proxy mới!"
            elif err_rate > 70:
                config.attack_stats["threat_intelligence"] = "Hệ thống phòng thủ của mục tiêu đã thích ứng. Cân nhắc dừng lại và chuyển sang chế độ 'Du kích'."
            elif total_ok > 100:
                config.attack_stats["threat_intelligence"] = "Tấn công đang diễn ra ổn định. Máy chủ mục tiêu đang chịu áp lực lớn. Tiếp tục duy trì!"
