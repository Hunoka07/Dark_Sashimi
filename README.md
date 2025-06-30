Dark Sashimi 1.0
Một công cụ kiểm tra hiệu năng Layer 7 thế hệ mới, được tích hợp AI Trợ chiến để phân tích và đề xuất các kế hoạch tác chiến thông minh.
⚠️ Tuyên bố Miễn trừ Trách nhiệm
> CẢNH BÁO: Công cụ này được tạo ra với mục đích duy nhất là GIÁO DỤC và NGHIÊN CỨU BẢO MẬT trong môi trường được cho phép. Tác giả tuyên bố từ chối mọi trách nhiệm đối với bất kỳ hành vi lạm dụng, phá hoại hoặc thiệt hại nào do công cụ này gây ra.
> NGƯỜI DÙNG PHẢI CHỊU HOÀN TOÀN TRÁCH NHIỆM PHÁP LÝ CHO MỌI HẬU QUẢ TỪ HÀNH ĐỘNG CỦA MÌNH.
> 
✨ Tính năng nổi bật
 * 🧠 AI Trợ chiến: Tự động phân tích sâu mục tiêu (WAF, cookies, nội dung HTML) để đưa ra kế hoạch tấn công tối ưu.
 * ⚔️ Vector Đa dạng: Tích hợp các vector tấn công L7 mạnh mẽ như HTTP Matrix và Slow Pipe.
 * 📊 Dashboard Chỉ huy: Theo dõi chiến dịch trong thời gian thực với giao diện trực quan, hiển thị các thông số quan trọng.
 * 🌐 Hỗ trợ Proxy: Tự động lấy và kiểm tra proxy từ nhiều nguồn uy tín để đảm bảo tính ẩn danh và hiệu quả.
 * 📱 Hoạt động không cần Root: Được thiết kế để hoạt động mạnh mẽ trên các thiết bị Android tiêu chuẩn mà không yêu cầu quyền root.
 * 🇻🇳 Giao diện Tiếng Việt: Toàn bộ giao diện được Việt hóa, thân thiện và dễ sử dụng.
🚀 Hướng dẫn Cài đặt & Triển khai
Để cài đặt và chạy Dark Sashimi, hãy làm theo chính xác các bước dưới đây.
Bước 1: Cài đặt Termux từ F-Droid
Nền tảng Termux trên Google Play đã cũ và không còn được hỗ trợ. Để đảm bảo công cụ hoạt động ổn định, bạn phải cài đặt Termux từ F-Droid.
 * Truy cập và tải về tại: https://f-droid.org/en/packages/com.termux/
Bước 2: Chuẩn bị Môi trường và Tải Công cụ
Mở ứng dụng Termux vừa cài đặt và sao chép toàn bộ khối lệnh dưới đây, sau đó dán vào Termux và nhấn Enter. Lệnh sẽ tự động chạy tuần tự.
# Cập nhật kho chứa gói (repository)
termux-change-repo

# Cập nhật và cài đặt các gói cần thiết
pkg update -y && pkg upgrade -y
pkg install git python libjpeg-turbo libcrypt -y

# Tải mã nguồn Dark Sashimi từ GitHub
git clone https://github.com/Hunoka07/Dark_Sashimi.git

# Di chuyển vào thư mục dự án
cd Dark_Sashimi

# Cài đặt các thư viện Python cần thiết
pip install -r requirements.txt

> Lưu ý: Khi lệnh termux-change-repo chạy, bạn có thể được yêu cầu chọn kho chứa. Hãy cứ nhấn Enter để chọn các lựa chọn mặc định.
> 
🎮 Hướng dẫn Sử dụng
Sau khi cài đặt thành công, bạn đã sẵn sàng để bắt đầu một chiến dịch.
Từ bên trong thư mục Dark_Sashimi, chạy lệnh sau:
python dark_sashimi.py

Công cụ sẽ khởi chạy. Hãy làm theo các hướng dẫn trên màn hình:
 * Nhập URL mục tiêu.
 * Xem báo cáo phân tích từ AI.
 * Quyết định làm theo kế hoạch của AI hoặc tự chọn chiến thuật.
 * Nhấn Enter để khai hỏa và theo dõi dashboard.
Để kết thúc chiến dịch bất cứ lúc nào, chỉ cần nhấn tổ hợp phím CTRL + C.
