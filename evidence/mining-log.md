# Mining log — VLearn Ready CP4

## Mục tiêu

Kiểm tra trong nguồn Tier-1 liệu Lesson 6 có sử dụng kiến thức nền mà không giải thích lại đầy đủ, có concept nào được dạy ngay trong lesson, và có nguồn review nội bộ để route hay không.

## Phạm vi và phương pháp

- Nguồn kiểm: `ai/fixtures/sources.json` gồm 4 artifact: Lesson 6 target, Lesson 3 transcript excerpt, Lesson 4 slide excerpt và Instructor Intent.
- Đơn vị quan sát: một statement nguyên văn trong artifact nói về dependency, cách lesson dạy concept, source review hoặc misconception.
- Rule `potential prerequisite gap`: lesson sử dụng/giả định một concept để theo task, không định nghĩa/giảng lại đủ trong lesson hiện tại, và có source review nội bộ xác định được.
- Không suy ra hành vi, tỷ lệ, thời gian hay mức đau của học viên từ log này.

## Kết quả mining

Đã kiểm 4 artifact và ghi nhận 5 observation có thể kiểm tra lại:

| # | Nguồn | Trích đoạn / sự kiện | Nhận định | Quyết định sản phẩm |
|---:|---|---|---|---|
| 1 | L6 `[02:10]` | “Bài dùng embedding để giảng dense retrieval mà **KHÔNG định nghĩa lại embedding**.” | Embedding là potential prerequisite gap | `Required`; route L3 18:40 |
| 2 | L6 `[Slide 6]` | “Bài giả định chunk 500 tokens, overlap 50 mà **không giảng lại chunking**.” | Chunking là potential prerequisite gap | `Required`; route L4 slide 14–17 |
| 3 | L6 `[09:00]` | “Reranking **được dạy kỹ trong bài**.” | Không phải kiến thức bắt buộc học trước | `Taught-in-lesson`; không ép review |
| 4 | L4 slide 14–17 | “Chunking xấu thì retrieval xấu dù reranker tốt.” | Dependency domain có hậu quả theo lesson | Giải thích vì sao route chunking quan trọng |
| 5 | Instructor Intent + L6 `[14:20]` | “Reranker **KHÔNG thay được retriever**”; retriever top-50, reranker top-5 | Misconception quan trọng được giảng viên nêu | Watchout + test C15/C17 |

## Giới hạn và việc tiếp theo

- Đây là content mining cho một target lesson và hai nguồn review; chưa đại diện cho toàn khóa.
- Chưa chứng minh pain/tần suất với người học. Nếu còn thời gian, bổ sung survey hoặc 5–10 tutor/Discord turns được phép dùng, lưu nguồn và phương pháp lọc.
- Nếu mở rộng mining, giữ nguyên rule ở trên và thêm từng observation vào bảng; không sửa các conclusion đã dùng để chấm CP4 mà không ghi changelog.
