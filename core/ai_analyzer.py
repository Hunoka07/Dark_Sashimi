# -*- coding: utf-8 -*-
import random

import config

class AIAnalyzer:
    def __init__(self, target_info):
        self.target_info = target_info
        self.plan = {
            "vector": "HTTP Matrix",
            "vector_id": "1",
            "mode": "Saturation",
            "threads": config.DEFAULT_THREADS["Saturation"],
            "threat_level": "[green]Thấp[/green]",
            "summary_report": "Mục tiêu không có lớp bảo vệ rõ ràng. Một cuộc tấn công bão hòa tiêu chuẩn được khuyến nghị."
        }

    def generate_plan(self):
        self.analyze_protection()
        self.analyze_latency()
        return self.plan

    def analyze_protection(self):
        protection = self.target_info.get("Bảo vệ", "")
        if "Cloudflare" in protection or "AWS WAF" in protection:
            self.plan["threat_level"] = "[bold yellow]Trung bình[/bold yellow]"
            self.plan["summary_report"] = "Mục tiêu được bảo vệ bởi một WAF mạnh. AI đề xuất tấn công 'Du kích' để tránh bị chặn và thăm dò phản ứng của hệ thống phòng thủ."
            self.plan["mode"] = "Guerilla"
            self.plan["threads"] = config.DEFAULT_THREADS["Guerilla"]
        elif "Sucuri" in protection:
            self.plan["threat_level"] = "[bold orange3]Cao[/bold orange3]"
            self.plan["summary_report"] = "Phát hiện lớp bảo vệ Sucuri. Đề xuất tấn công 'Hủy diệt' với số luồng cực lớn để thử vượt qua bộ đệm cache và giới hạn tốc độ của họ."
            self.plan["mode"] = "Annihilation"
            self.plan["threads"] = config.DEFAULT_THREADS["Annihilation"]

    def analyze_latency(self):
        try:
            latency_str = self.target_info.get("Độ trễ TB", "0 ms").split()[0]
            latency = float(latency_str)
            if latency > 500:
                self.plan["threat_level"] = "[bold red]Rất cao[/bold red]"
                self.plan["vector"] = "Slow Pipe"
                self.plan["vector_id"] = "2"
                self.plan["summary_report"] = "Độ trễ của mục tiêu rất cao, cho thấy máy chủ đã quá tải hoặc ở xa. Vector 'Slow Pipe' sẽ cực kỳ hiệu quả để làm cạn kiệt tài nguyên kết nối còn lại của nó."
                self.plan["mode"] = "Saturation"
                self.plan["threads"] = int(config.DEFAULT_THREADS["Saturation"] / 2) # Slowloris cần ít luồng hơn
        except (ValueError, IndexError):
            pass


