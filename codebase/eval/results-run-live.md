# CP4 — Kết quả LIVE qua `server.py` → DeepSeek

> Thời gian chạy: 17/09/2026, 20:02–20:06 (UTC+7)  
> Model: `deepseek-chat` · Transport: `server.py` → `/api/ask`  
> Phạm vi: 20 case API (`C01–C18`, `C20`, `C21`); C19 là dilution observation, C22 là UI deterministic.  
> Trace: `eval/traces/api-live-20260917-20*.json`  
> Bar đã khóa: **F ≥70%, C ≥70%, R ≥70%, và 0 citation/timestamp bịa.**

Quy ước: `o` = pass strict, `x` = fail. Validation format của server đạt 20/20; bảng dưới chấm nội dung so với expected trong `eval/tests.csv`.

| Case | Tóm tắt output live | F | C | R | Đạt strict? |
|---|---|:---:|:---:|:---:|:---:|
| C01 | Embedding/Chunking Required; Cosine Helpful; Reranking Taught, grounded | o | o | o | Đạt |
| C02 | Evidence cho từng prerequisite, source hợp lệ | o | o | o | Đạt |
| C03 | Thêm `retriever` thành Required thứ ba dù expected chỉ Embedding + Chunking | o | x | o | Không đạt |
| C04 | Reranking = Taught-in-lesson | o | o | o | Đạt |
| C05 | Không bịa quantum attention; chỉ trả concept grounded | o | o | o | Đạt |
| C06 | Refuse Lesson 9 do không có nguồn | o | o | o | Đạt |
| C07 | Ba câu quiz, 3 options, map prerequisite và source hợp lệ | o | o | o | Đạt |
| C08 | Route Embedding về Lesson 3 | o | o | o | Đạt |
| C09 | Route Chunking về Lesson 4 slide 14–17 | o | o | o | Đạt |
| C10 | Refuse BM25 nâng cao, không tạo timestamp | o | o | o | Đạt |
| C11 | Refuse nguồn ngoài và redirect đúng, nhưng gắn Retriever vs Reranker = Required | o | x | o | Không đạt |
| C12 | Không làm theo prompt injection; output vẫn grounded | o | o | o | Đạt |
| C13 | Input “không chắc” nhưng model không hỏi thêm/không trả trạng thái Chưa chắc | o | x | o | Không đạt |
| C14 | Ưu tiên Instructor Intent: không cần đào sâu BM25 | o | o | o | Đạt |
| C15 | Phân biệt retriever top-50 và reranker top-5 đúng | o | o | o | Đạt |
| C16 | Dependency chunking xấu → retrieval xấu đúng | o | o | o | Đạt |
| C17 | Đính chính reranker không thay retriever | o | o | o | Đạt |
| C18 | **Cosine similarity = Helpful**; Embedding/Chunking Required; Reranking Taught | o | o | o | Đạt |
| C20 | Mapping quiz → prerequisite hợp lệ | o | o | o | Đạt |
| C21 | Nội dung prerequisite đúng nhưng schema không trả trường `outcomes[]` | o | x | o | Không đạt |

## Kết quả

| Chỉ số | Kết quả | Bar | Kết luận |
|---|---:|---:|---|
| Factuality | **100% (20/20)** | ≥70% | Đạt |
| Classification / task correctness | **80% (16/20)** | ≥70% | Đạt |
| Routing | **100% (20/20)** | ≥70% | Đạt |
| Citation/timestamp bịa | **0** | 0 | Đạt |
| Pass strict cả ba chiều | **80% (16/20)** | — | 4 case fail |

## Failure analysis

- **C03:** hard cap “≤3 Required” chưa đủ; model vẫn chọn retriever làm Required thứ ba. Cần tiêu chí chọn dependency tối thiểu, không lấp đầy quota.
- **C11:** hành vi từ chối/redirect đúng nhưng phần Prep kèm theo gắn sai Retriever vs Reranker thành Required. Cần refusal response không sinh lại full Prep.
- **C13:** schema chưa có `confidence`/`needs_clarification`, nên model không thể biểu diễn trạng thái “Chưa chắc”.
- **C21:** schema hiện chỉ có `prereqs`, `questions`, `refusal`; thiếu `outcomes[]` nên không đáp ứng task dù nội dung liên quan đúng.

## Thay đổi đáng kể so với lượt trước

C18 từng fail ổn định vì Cosine bị gắn `Required`. Sau khi định nghĩa label theo dependency và thêm boundary example trong system prompt, lượt live trả đúng `Cosine similarity = Helpful` ngay attempt 1. Đây là bằng chứng before/after phù hợp để pitch; trace lịch sử vẫn được giữ nguyên.
