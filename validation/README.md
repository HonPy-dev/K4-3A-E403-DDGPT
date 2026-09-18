# Validation protocol — VLearn Ready

> **Cảnh báo dữ liệu:** Các dòng hiện có trong `feedback-log.csv` là dữ liệu mô phỏng để kiểm thử cấu trúc và luồng hiển thị, không phải bằng chứng người dùng thật và không được dùng để nộp validation. Chỉ thay thế cảnh báo này sau khi đã có consent và phản hồi thực tế.

## Đối tượng và consent

Mời hai học viên AI20k ngoài nhóm. Trước khi test, đọc nội dung sau và chỉ bắt đầu khi người tham gia đồng ý:

> Tôi đồng ý thử prototype VLearn Ready trong khoảng 10 phút. Nhóm có thể lưu phản hồi của tôi dưới mã ẩn danh U01/U02 để phục vụ hackathon. Tôi hiểu rằng phản hồi không ảnh hưởng kết quả học tập và có thể yêu cầu nhóm ngừng ghi nhận bất kỳ lúc nào.

Người điều phối ghi `consent_confirmed=true`, thời gian và đường dẫn ảnh/ghi chú consent vào `feedback-log.csv`. Không thu email, số điện thoại hoặc tên nếu không cần thiết.

## Nhiệm vụ test

1. Mở Lesson 6 · RAG + Reranking từ dashboard.
2. Bấm **Chuẩn bị bài (AI live)** và đọc Prep Card.
3. Nói thành tiếng sự khác nhau giữa Required, Helpful và Taught-in-lesson.
4. Làm ba câu Readiness Check mà không được người điều phối gợi ý.
5. Nếu được route ôn tập, mở nguồn review và kiểm tra có đúng lesson/đoạn cần xem không.
6. Vào lesson hoặc chọn bỏ qua Prep.

## Điều kiện hoàn thành

- `prep_opened=true` khi card mở và có nội dung.
- `labels_understood=true` khi người thử diễn giải đúng ba label bằng lời của họ.
- `quiz_completed=true` khi nộp đủ ba câu.
- `review_source_opened=true` khi mở đúng nguồn được route; ghi `not_applicable` nếu verdict READY.
- `lesson_entered=true` khi flow kết thúc ở lesson.
- Ghi thời gian từ lúc mở card đến lúc đưa ra quyết định vào bài/ôn lại.

## Câu hỏi sau test

1. Card giúp bạn quyết định xem lại phần nào không? Vì sao?
2. Label hoặc nguồn nào khiến bạn chưa tin hay chưa hiểu?
3. Nếu dùng trước một lesson thật, bạn muốn bỏ, giữ hay đổi phần nào?

Ghi câu trả lời nguyên văn vào `verbatim_feedback`; không viết lại thành lời tích cực hơn. `usefulness_1_to_5` và `trust_1_to_5` do người tham gia tự chọn.
