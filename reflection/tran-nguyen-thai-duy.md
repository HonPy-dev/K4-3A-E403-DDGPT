# Reflection — Trần Nguyễn Thái Duy — 2A202602991

> Bản nháp cá nhân: thành viên cần đọc lại và xác nhận nội dung trước khi nộp.

## Vai trò và đóng góp

Tôi phụ trách prompt, grounding và kiểm tra các phản hồi của mô hình. Tôi xây dựng cách giới hạn nguồn Tier-1, yêu cầu JSON có cấu trúc và kiểm tra citation trước khi kết quả được đưa lên giao diện. Tôi cũng tham gia chạy golden set và lưu trace để mỗi kết luận đều có thể truy ngược.

## Điều tôi học được

Một prompt rõ chưa đủ để tạo sản phẩm AI đáng tin cậy. Hệ thống còn cần allowlist nguồn, validator và tình huống từ chối khi thiếu căn cứ. Việc giữ lại các case thất bại giúp nhóm thấy lỗi phân loại Helpful/Required có tính lặp lại và sửa đúng nguyên nhân.

## Điều chưa tốt và hướng cải thiện

Một số case mơ hồ vẫn không đạt strict vì mô hình trả lời hợp lý nhưng sai format hoặc quyết định quá mạnh. Nếu có thêm thời gian, tôi sẽ tách confidence khỏi label, bổ sung regression test cho C03/C11/C13/C21 và thử nhiều lần chạy để đo độ ổn định.
