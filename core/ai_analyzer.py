# -*- coding: utf-8 -*-
import re
import config

class AIAnalyzer:
    def __init__(self, target_info, response_obj):
        self.target_info = target_info
        self.response = response_obj
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
        headers = {k.lower(): v for k, v in self.response.headers.items()}
        content = self.response.text.lower()
        
        if headers.get("server") == "cloudflare" or "cf-ray" in headers:
            self.plan["threat_level"] = "[bold yellow]Trung bình[/bold yellow]"
            self.plan["summary_report"] = "Phát hiện Cloudflare. AI đề xuất tấn công 'Du kích' để tránh kích hoạt cơ chế chống bot và thăm dò phản ứng của hệ thống phòng thủ."
            self.plan["mode"] = "Guerilla"
            self.plan["threads"] = config.DEFAULT_THREADS["Guerilla"]
        elif "sucuri" in headers.get("x-sucuri-id", ""):
            self.plan["threat_level"] = "[bold orange3]Cao[/bold orange3]"
            self.plan["summary_report"] = "Phát hiện lớp bảo vệ Sucuri. Đề xuất tấn công 'Hủy diệt' với số luồng cực lớn để thử vượt qua bộ đệm cache và giới hạn tốc độ của họ."
            self.plan["mode"] = "Annihilation"
            self.plan["threads"] = config.DEFAULT_THREADS["Annihilation"]
        elif "aws" in headers.get("server", "") or "x-amz-cf-id" in headers:
            self.plan["threat_level"] = "[bold yellow]Trung bình[/bold yellow]"
            self.plan["summary_report"] = "Hệ thống có vẻ đang sử dụng AWS WAF/CloudFront. Cần tấn công một cách thông minh. Đề xuất chế độ 'Bão hòa' để tạo áp lực vừa đủ."
            self.plan["mode"] = "Saturation"
            self.plan["threads"] = config.DEFAULT_THREADS["Saturation"]
        elif re.search(r'<meta name="generator" content="WordPress', content, re.IGNORECASE):
            self.plan["threat_level"] = "[green]Thấp-Trung bình[/green]"
            self.plan["summary_report"] = "Phát hiện website WordPress. Các trang này thường dễ bị tấn công vào file xmlrpc.php hoặc wp-login.php. Tuy nhiên, AI khuyến nghị một cuộc tấn công 'Bão hòa' tổng lực trước."
            self.plan["mode"] = "Saturation"

    def analyze_latency(self):
        try:
            latency_str = self.target_info.get("Độ trễ TB", "0 ms").split()[0]
            latency = float(latency_str)
            if latency > 600:
                self.plan["threat_level"] = "[bold red]Rất cao[/bold red]"
                self.plan["vector"] = "Slow Pipe"
                self.plan["vector_id"] = "2"
                self.plan["summary_report"] = "Độ trễ của mục tiêu rất cao, cho thấy máy chủ đã quá tải hoặc ở xa. Vector 'Slow Pipe' sẽ cực kỳ hiệu quả để làm cạn kiệt tài nguyên kết nối còn lại của nó."
                self.plan["mode"] = "Saturation"
                self.plan["threads"] = int(config.DEFAULT_THREADS["Saturation"] / 2)
        except (ValueError, IndexError):
            pass


