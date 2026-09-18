# Competitive research — CP4

Ngày rà soát: 17/09/2026  
Phương pháp: desk research trên tài liệu chính thức và đối chiếu với flow VLearn Ready. Log này không tuyên bố đã hoàn thành user test có đăng nhập trên Khanmigo.

## ChatGPT Study Mode

Nguồn chính thức:

- OpenAI Help Center — https://help.openai.com/en/articles/11780217
- OpenAI product announcement — https://openai.com/index/chatgpt-study-mode/

Flow quan sát từ tài liệu: người học bật Study trong cuộc hội thoại, cung cấp mục tiêu/trình độ/tài liệu, hệ thống dùng câu hỏi dẫn dắt, giải thích theo lớp và knowledge checks để kiểm tra hiểu biết. Người dùng có thể bật/tắt chế độ trong cuộc hội thoại.

Điểm đáng học:

1. Hỏi điều người học đã biết trước khi giải thích để calibrate độ sâu.
2. Dùng câu hỏi và phản hồi để người học tự suy luận thay vì chỉ đưa đáp án.
3. Chia nội dung phức tạp thành phần nhỏ, giảm cognitive load.
4. Nói rõ giới hạn: chế độ học vẫn có thể sai và cần kiểm tra thông tin quan trọng.

Điểm VLearn Ready chọn khác:

- Bắt đầu trước lesson và chỉ giải một quyết định: prerequisite nào cần biết trước.
- Nguồn bị giới hạn vào transcript/slide/Instructor Intent của khóa.
- Route tới đúng Lesson/timestamp thay vì hội thoại học tập mở.
- Prep luôn có thể bỏ qua; hệ thống không chặn người học vào lesson.

## Khanmigo

Nguồn chính thức:

- Khan Academy — https://www.khanacademy.org/khan-labs
- Khan Academy Help Center — https://support.khanacademy.org/hc/en-us/articles/25921448458893-What-features-are-available-in-the-Learner-Parent-and-Teacher-Khanmigo-subscription-plans
- Khanmigo Community Guidelines — https://support.khanacademy.org/hc/en-us/articles/13860282793869-What-are-the-Community-Guidelines-for-Khanmigo

Flow quan sát từ tài liệu: Khanmigo đóng vai trò tutor, đưa hint/câu hỏi/giải thích để phát triển tư duy độc lập và gắn với thư viện nội dung Khan Academy. Hệ thống ưu tiên dẫn dắt thay vì đưa đáp án trực tiếp.

Điểm đáng học:

1. Gắn AI với content library đáng tin cậy thay vì web mở.
2. Giữ người học tham gia chủ động bằng câu hỏi và hint.
3. Phân biệt rõ công cụ cho learner và teacher.

Điểm VLearn Ready chọn khác:

- Không cố trở thành tutor toàn bài; chỉ tạo một bước chuẩn bị 2–5 phút.
- Phân loại rõ `Required`, `Helpful`, `Taught-in-lesson` để tránh chuẩn bị thừa.
- Citation allowlist và trace là điều kiện pass, không chỉ là phần trình bày.

## Quyết định thiết kế rút ra

| Quan sát | Quyết định trong VLearn Ready | Vị trí kiểm chứng |
|---|---|---|
| Tutor tốt cần người học tham gia | Prep đi kèm 3 readiness questions | `vlearn_ready.js` |
| Grounding vào nội dung khóa giảm lệch | Chỉ dùng source allowlist L6/L3/L4/INTENT | `ai/ai_call.py`, `ai/fixtures/sources.json` |
| Hệ thống vẫn có thể sai | Hiển thị nguồn, fallback, lưu trace và giữ C18 fail trong báo cáo | `server.py`, `eval/traces/`, `spec.md` |
| User cần quyền kiểm soát | Luôn có “Bỏ qua & Vào học ngay” và “Kiểm tra lại” | `vlearn_ready.js` |

## Giới hạn nghiên cứu

Đây là desk research từ tài liệu sản phẩm chính thức. Muốn ghi “dùng thử trực tiếp”, nhóm cần lưu ngày, tài khoản/plan, prompt, screenshot hoặc transcript phiên dùng thử; không suy diễn từ tài liệu thành trải nghiệm đã thực hiện.
