import threading
import time
from urllib.parse import urlparse
import psutil
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

import config

console = Console()

def display_main_banner():
    banner = """
██████╗  █████╗ ██████╗ ██╗  ██╗    ███████╗  █████╗  ███████╗ ██╗  ██╗ ██╗ ███╗   ██║
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██╔════╝ ██╔══██╗██╔════╝ ██║  ██║ ██║ ████╗  ██║
██║  ██║███████║██████╔╝█████╔╝     ███████╗ ███████║███████╗ ███████║ ██║ ██╔██╗ ██║
██║  ██║██╔══██║██╔══██╗██╔═██╗     ╚════██║ ██╔══██║╚════██║ ██╔══██║ ██║ ██║╚██╗██║
██████╔╝██║  ██║██║  ██║██║  ██╗    ███████║ ██║  ██║███████║ ██║  ██║ ██║ ██║ ╚████║
╚═════╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝ ╚═╝  ╚═╝╚══════╝ ╚═╝  ╚═╝ ╚═╝ ╚═╝  ╚═══╝                                                                     
    """
    console.print(Text(banner, style="bold magenta"), justify="center")
    console.print(Text(f"Layer 7 Performance Testing Tool - {config.CREATOR}", style="bold cyan"), justify="center")
    console.print("-" * 80)

def get_system_panel():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return Panel(Text(f"CPU: [white]{cpu: >5.1f}%[/white]\nRAM: [white]{ram: >5.1f}%[/white]"), title="[b]System[/b]", border_style="yellow")

def get_attack_stats_panel():
    elapsed = max(time.time() - config.attack_stats["start_time"], 1)
    rps = config.attack_stats["requests_sent"] / elapsed
    sps = config.attack_stats["sockets_opened"] / elapsed
    
    data_sent = config.attack_stats["bytes_sent"]
    if data_sent > 1024**3: data_str = f"{data_sent / 1024**3:.2f} GB"
    elif data_sent > 1024**2: data_str = f"{data_sent / 1024**2:.2f} MB"
    else: data_str = f"{data_sent / 1024:.2f} KB"
    
    rate_str = f"{data_sent / elapsed / 1024**2:.2f} MB/s"

    table = Table(show_header=False, show_edge=False, box=None)
    table.add_column(style="cyan", justify="right")
    table.add_column(style="bold white", justify="left")
    table.add_row("HTTP RPS :", f" {rps:,.1f}")
    table.add_row("Sockets/s :", f" {sps:,.1f}")
    table.add_row("Errors :", f" {config.attack_stats['errors']:,}")
    table.add_row("Threads :", f" {config.attack_stats['active_threads']}")
    table.add_row("Data Sent :", f" {data_str}")
    table.add_row("Bandwidth :", f" {rate_str}")

    return Panel(table, title="[b]Live Statistics[/b]", border_style="green")

def update_threat_intelligence():
    total_requests = config.attack_stats.get("requests_sent", 0)
    total_sockets = config.attack_stats.get("sockets_opened", 0)

    if total_sockets > 0 and total_requests == 0:
        if config.attack_stats["errors"] > total_sockets * 0.5:
             config.attack_stats["threat_intelligence"] = "High socket error rate. Target may be resetting connections. Verify port and firewall rules."
        else:
             config.attack_stats["threat_intelligence"] = "Slowloris sockets established. Server connection pool is under pressure."
    
    elif total_requests > 10:
        err_rate = (config.attack_stats["errors"] / total_requests * 100)
        if err_rate > 80: config.attack_stats["threat_intelligence"] = "Critical error rate. Proxies may be blocked or target is behind aggressive WAF. Check proxy quality."
        elif err_rate > 50: config.attack_stats["threat_intelligence"] = "High error rate. Target is likely throttling. Consider 'Stealth' mode to appear less aggressive."
        else: config.attack_stats["threat_intelligence"] = "HTTP Flood is effective. Target is responding. Maintain pressure."

def run_dashboard_loop():
    layout = Layout(name="root")
    layout.split(Layout(name="header", size=5), Layout(ratio=1, name="main"), Layout(size=3, name="footer"))
    layout["main"].split_row(Layout(name="side"), Layout(name="body", ratio=2))
    layout["side"].split(Layout(name="sys_info"), Layout(name="intel"))

    layout["header"].update(Panel(Text(f"DARK SASHIMI {config.VERSION}", justify="center", style="bold magenta on black")))
    layout["footer"].update(Panel(Text("Press [bold]CTRL+C[/bold] to terminate operation.", justify="center", style="yellow")))
    
    with Live(layout, screen=True, redirect_stderr=False, vertical_overflow="visible", refresh_per_second=4) as live:
        while not config.stop_event.is_set():
            update_threat_intelligence()
            layout["body"].update(get_attack_stats_panel())
            layout["sys_info"].update(get_system_panel())
            layout["intel"].update(Panel(Text(config.attack_stats['threat_intelligence'], style="italic magenta"), title="[b]Threat Intel[/b]", border_style="blue"))
            time.sleep(0.25)

def launch_dashboard():
    dashboard_thread = threading.Thread(target=run_dashboard_loop, daemon=True)
    dashboard_thread.start()
    return dashboard_thread
