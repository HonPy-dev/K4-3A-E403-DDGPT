# Reflection — Từ Hoàng Giang — 2A202602363


## Vai trò và đóng góp

Tôi phụ trách evaluation và chuẩn bị demo. Tôi rà golden set, chấm ba chiều Factuality, Classification và Routing, tổng hợp metrics và giữ lại trace của cả pass lẫn fail. Tôi cũng theo dõi các case khó để kết quả đo phản ánh đúng chất lượng thay vì chỉ chọn ví dụ đẹp.

## Điều tôi học được

Một tỷ lệ pass chung có thể che khuất lỗi quan trọng. Tách F/C/R cho thấy hệ thống không bịa citation nhưng vẫn có thể phân loại sai hoặc xử lý mơ hồ chưa tốt. Failure analysis của C03/C11/C13/C21 có giá trị trực tiếp cho vòng cải tiến tiếp theo.

## Điều chưa tốt và hướng cải thiện

Lượt đo hiện có một lần chạy chính và một số case cần chấm thủ công. Nếu tiếp tục, tôi sẽ thêm người chấm thứ hai, ghi cách giải quyết bất đồng và chạy lặp để báo confidence interval thay vì chỉ một điểm số.
