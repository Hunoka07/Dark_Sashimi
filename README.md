Tonu

Một công cụ ddos nguy hiểm sử dụng layer 7, được tích hợp AI để giúp phân tích và đưa ra phương hướng tấn công.

 ⚠️ Tuyên bố Miễn trừ Trách nhiệm

> CẢNH BÁO: Công cụ này được tạo ra với mục đích duy nhất là Tấn Công Web trong môi trường được cho phép. Tác giả tuyên bố từ chối mọi trách nhiệm đối với bất kỳ hành vi lạm dụng, phá hoại hoặc thiệt hại nào do công cụ này gây ra.
>
> NGƯỜI DÙNG PHẢI CHỊU HOÀN TOÀN TRÁCH NHIỆM PHÁP LÝ CHO MỌI HẬU QUẢ TỪ HÀNH ĐỘNG CỦA MÌNH.

🚀 Hướng dẫn Cài đặt & Triển khai
Để cài đặt và chạy Tonu 1.0, hãy làm theo chính xác các bước dưới đây.

Bước 1: Cài đặt Termux từ F-Droid
Nền tảng Termux trên Google Play đã cũ và không còn được hỗ trợ. Để đảm bảo công cụ hoạt động ổn định, bạn phải cài đặt Termux từ F-Droid.
  
  Truy cập và tải về tại: https://f-droid.org/en/packages/com.termux/

Bước 2: Chuẩn bị Môi trường và Tải Công cụ

Mở ứng dụng Termux vừa cài đặt và sao chép toàn bộ khối lệnh dưới đây, sau đó dán vào Termux và nhấn Enter. Lệnh sẽ tự động chạy tuần tự.

Cập nhật và cài đặt các gói cần 
thiết

pkg update -y && pkg upgrade -y
pkg install git python libjpeg-turbo libcrypt -y

 Tải mã nguồn Tonu từ GitHub
git clone https://github.com/Hunoka07/Tonu.git

 Di chuyển vào thư mục dự án
cd Tonu

 Cài đặt các thư viện Python cần thiết
pip install -r requirements.txt

🎮 Hướng dẫn Sử dụng
Sau khi cài đặt thành công, bạn đã sẵn sàng để bắt đầu một chiến dịch.
Từ bên trong thư mục Tonu, chạy lệnh sau:
python tonu.py

Công cụ sẽ khởi chạy. Hãy làm theo các hướng dẫn trên màn hình:
  Nhập URL mục tiêu.
  Xem báo cáo phân tích từ AI.
  Quyết định làm theo kế hoạch của AI hoặc tự chọn chiến thuật.
  Nhấn Enter để khai hỏa và theo dõi dashboard.
Để kết thúc chiến dịch bất cứ lúc nào, chỉ cần nhấn tổ hợp phím CTRL + C.
