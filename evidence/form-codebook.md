# Survey codebook

Nguồn câu hỏi: Google Form “Khảo sát trải nghiệm chuẩn bị trước một bài học trên VLearn”.

| Cột CSV | Câu hỏi form | Kiểu dữ liệu |
|---|---|---|
| `eligible_ai20k_outside_team` | Có phải học viên AI20k và không thuộc nhóm? | yes/no |
| `active_last_14_days` | Có học ít nhất một lesson trong 14 ngày? | yes/no |
| `last_lesson` | Lesson gần nhất | category |
| `prep_actions` | Trước lesson thực tế đã làm gì? | multi-select, phân tách bằng `|` |
| `unknown_before_lesson` | Điều chưa biết rõ trước lesson | multi-select |
| `gap_frequency_14d` | Số lần đang học mới nhận ra thiếu concept | 1 / 2–3 / ≥4 / 0 / không nhớ |
| `concept_group` | Nhóm concept chưa hiểu | multi-select |
| `discovery_point` | Đầu / giữa / cuối / nhiều đoạn | category |
| `response_actions` | Hành động khi gặp gap | multi-select |
| `first_source` | Nguồn đầu tiên dùng để tìm hiểu | category |
| `source_helpfulness` | Nguồn đầu tiên có giúp học tiếp không? | category |
| `time_lost_band` | Thời gian mất thêm | 0 / <5 / 5–10 / 11–20 / >20 / không nhớ |
| `learning_impact` | Ảnh hưởng đến mạch học | category |
| `desired_prep_info` | Thông tin giúp chuẩn bị tốt hơn | multi-select |
| `search_difficulty` | Điều khiến tìm đúng phần khó nhất | category |
| `willing_to_test` | Đồng ý dùng thử 10 phút? | yes / maybe / no |
| `verbatim_quote` | Quote gốc nếu response export có câu tự do/phỏng vấn follow-up | text nguyên văn |
| `consent_for_research` | Consent lưu/quote phản hồi | yes/no + nguồn xác nhận |
| `source_record` | Dòng/sheet/timestamp dùng để truy vết | text |

Google Form hiện không có câu hỏi mở lấy quote và không có câu consent sử dụng quote. Vì vậy `verbatim_quote` và `consent_for_research` phải đến từ follow-up có lưu bằng chứng, không được suy ra từ lựa chọn trắc nghiệm.
