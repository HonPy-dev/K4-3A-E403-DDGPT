# VLearn Ready — codebase chấm prototype

Thư mục này chứa bản prototype chạy độc lập dùng để chấm R5. Bản ở root được giữ lại để tương thích với quá trình phát triển; nội dung trong `codebase/` là bản nộp theo cấu trúc yêu cầu.

## Chạy nhanh

```powershell
cd codebase
$env:DEEPSEEK_API_KEY="<your-key>"
python server.py
```

Mở `http://localhost:3000`. Kiểm tra trước bằng `http://localhost:3000/api/health`.

Không có key hoặc mất mạng, giao diện chuyển sang dữ liệu fallback đã kiểm tra và hiển thị banner vàng. Khi API trả kết quả thật, giao diện hiển thị banner AI live cùng tên trace.

## Thành phần được chấm

- `index.html`: dashboard và điểm vào VLearn Ready.
- `vlearn_ready_mock.html`: lát cắt Lesson Prep → readiness quiz → review → lesson.
- `vlearn_ready.js`, `vlearn_ready.css`: logic và giao diện prototype.
- `server.py`: static server và API proxy DeepSeek.
- `ai/`: prompt, fixtures, validation và runner.
- `eval/`: golden set, metrics và traces mà server cần đọc.
- `assets/`: CSS, font và hình ảnh giao diện cục bộ. Video bài học gốc không được đưa vào bản nộp công khai; các vùng video chỉ là phần minh họa của prototype.

## Phần AI và phần fallback

- **AI live:** tạo Prep JSON từ bốn nguồn allowlist, phân loại `Required`, `Helpful`, `Taught-in-lesson`, kiểm tra citation và lưu trace.
- **Deterministic:** chấm readiness quiz và điều hướng READY/PARTIALLY/NOT READY.
- **Fallback/mock:** dùng `ai/prep-cp3.json` khi thiếu key, lỗi mạng hoặc output không đạt validation; trạng thái được ghi rõ trên UI.

API key chỉ được đọc từ biến môi trường hoặc `.env` cục bộ. Không đưa `.env` vào repo.
