from rich.console import Console
from rich.panel import Panel
from core.analytics import TargetAnalytics
from core.ai_analyzer import AIAnalyzer
from core.attack_manager import AttackManager
from utils.network import ProxyManager, fetch_user_agents
import config
import time

console = Console()

def main():
    console.clear()
    console.print(Panel.fit(
        f"{config.PROJECT_NAME}\n{config.CREATOR}\nPhiên bản: {config.VERSION}",
        title="🚀 Dark Sashimi", title_align="left")
    )
    while True:
        target_url = console.input("Nhập URL mục tiêu (bao gồm http/https, hoặc bấm Enter để thoát): ").strip()
        if not target_url:
            console.print("Không có URL, thoát!")
            return
        fetch_user_agents()
        ProxyManager().load_proxies()
        analytics = TargetAnalytics(target_url)
        target_info, response_obj = analytics.run_analysis()
        if not target_info or not response_obj:
            console.print("Không thể phân tích mục tiêu!")
            continue
        plan = AIAnalyzer(target_info, response_obj).generate_plan()
        console.print(Panel.fit(
            f"AI Đề Xuất Chiến Dịch:\n"
            f"• Vector: {plan['vector']}\n"
            f"• Threads: {plan['threads']}\n"
            f"• Mode: {plan['mode']}\n"
            f"• Threat Level: {plan['threat_level']}\n"
            f"• Report: {plan['summary_report']}", title="🤖 AI Battle Plan"))
        confirm = console.input("Bắt đầu tấn công? (y/n): ").strip().lower()
        if confirm != "y":
            console.print("Chiến dịch đã huỷ.")
            continue
        time.sleep(1)
        attack = AttackManager(
            target_url=target_url,
            vector_choice=plan["vector_id"],
            mode=plan["mode"],
            threads=plan["threads"]
        )
        attack.start_attack()
        console.print(Panel.fit("Chiến dịch đã kết thúc!"))
        again = console.input("Tấn công mục tiêu khác? (y/n): ").strip().lower()
        if again != "y":
            break

if __name__ == "__main__":
    main()
