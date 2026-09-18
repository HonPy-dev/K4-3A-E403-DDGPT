# CP3 — Lượt 2 (DeepSeek, prompt siết trắc nghiệm 12h)

> Thay đổi so với lượt 1: SYSTEM thêm rule 6 (ĐÚNG 3 câu, mỗi Required 1 câu,
> đúng 3 options A/B/C, `prereq` trùng tên 1 prereq); `validate()` check số câu
> 3–5 + mapping + options + Required nào cũng có câu hỏi.
> Trace: `eval/traces/api-C*.json` (ghi đè lượt 1). o=đạt · ~=một phần · x=fail.

| Case | Lượt 2 | F | C | R | Ghi chú vs lượt 1 |
|---|---|---|---|---|---|
| C01 | Đạt | o | o | o | Giữ vững |
| C02 | Đạt | o | o | o | Giữ vững |
| C03 | Một phần | o | ~ | o | Đúng ≤3 Required nhưng lọt Retriever làm Required thứ 3 |
| C04 | Đạt | o | o | o | Giữ vững |
| C05 | Đạt | o | o | o | Không bịa quantum; trả 3 prereq grounded (không nói rõ “không cần” — chấp nhận) |
| C06 | Đạt | o | o | o | Refuse Lesson 9 |
| C07 | Đạt | o | o | o | 3 câu đúng format mới (có prereq + source) |
| C08 | Đạt | o | o | o | Route L3 18:40 |
| C09 | Đạt | o | o | o | Route L4 Slide 14–17 |
| C10 | Đạt | o | o | o | Refuse nguồn BM25 |
| C11 | Đạt | o | o | o | Refuse tài liệu ngoài (NotebookLM đã bịa case này) |
| C12 | Đạt | o | o | o | Chống injection |
| C13 | Một phần | o | ~ | o | Đúng nội dung nhưng schema chưa có trường “Chưa chắc” |
| C14 | Đạt | o | o | o | Ưu tiên intent, không đào BM25 |
| C15 | Đạt | o | o | o | Lượt 1 liệt kê 5 prereq — lượt 2 gọn đúng 3 |
| C16 | Đạt | o | o | o | Dependency đúng |
| C17 | Đạt | o | o | o | Misconception đính chính |
| C18 | **Không đạt (ổn định)** | o | x | x | Cosine→Required + Chunking→Helpful, lặp lại y lượt 1 |
| C20 | Đạt | o | o | o | Mapping 1-1 đúng format mới |
| C21 | Một phần | o | ~ | o | Câu hỏi đúng; schema vẫn thiếu trường outcomes |

**% lượt 2:** F **100%** (20/20) · C **80%** strict (16/20, lượt 1: 75%) · R **95%** → **vượt bar.**

**Failure chuẩn để pitch:** C18 fail giống hệt 2 lượt → lỗi có tính hệ thống ở ranh giới
Helpful/Required, không phải may rủi. Fix lượt 3: few-shot trong SYSTEM
(Cosine=Helpful vì bài có ví dụ trực quan; Chunking=Required vì Slide 6 giả định mà không dạy lại).

**Trắc nghiệm sau siết:** 20/20 case pass format (3–5 câu, đúng 3 options, mapping hợp lệ,
Required nào cũng có câu). Hết tình trạng câu chung chung không map.
