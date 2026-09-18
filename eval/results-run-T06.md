# Lượt T06 — data THẬT (transcript T06/T04 + slide, không chatlog)

> Pipeline: `ai/extract.py --lesson T06` → 31.378 chars (T06 20K + T04 7K + slide 4K)
> → DeepSeek `deepseek-chat` full-context (không retrieval → không dilution).
> Trace: `eval/traces/api-T06-T*.json`. o=đạt · ~=một phần.
> Bar: ≥70% cả 3 chiều, 0 bịa. Kiểm toàn mã cite bằng script (39 mã thật, AI cite 7 mã).

| Case | Kết quả | F | C | R | Ghi chú |
|---|---|---|---|---|---|
| T01 | Một phần | o | ~ | o | Prereq đúng + cite mã thật ở trường source, nhưng evidence thiếu mã inline (validator FAIL). Cùng prompt chạy 2 lần ra 2 dạng → minh chứng non-determinism |
| T02 | Đạt | o | o | o | Evidence đủ mã, 5 câu (trong hạn 3–5) |
| T03 | Đạt | o | o | o | Đúng ≤3 Required (+2 Helpful) |
| T04 | Đạt | o | o | o | Self-attention QKV = Taught-in-lesson (T06 dạy + lab) |
| T05 | Đạt | o | o | o | Refuse 'quantum backprop' đúng |
| T06 | Đạt | o | o | o | Refuse ngoài phạm vi đúng |
| T07 | Đạt | o | o | o | 3 câu mapping 1-1 + cite mã (Duy đối chiếu) |
| T08 | Đạt | o | o | o | Route token về slide (chấp nhận; kỳ vọng T04 — slide cũng đúng) |
| T09 | Đạt | o | o | o | Refuse timestamp 'softmax temperature', không bịa mã |
| T10 | Một phần | o | ~ | o | Đúng hướng nhưng cần Duy đối chiếu misconception hallucination với transcript |

**% lượt T06 (10 case):** F **100%** (citation thật, script kiểm 0 mã bịa) ·
C **~80%** (8/10, T01+T10 partial) · R **~90%**.

**Khác biệt vs fixture (RAG):**
1. AI trích mã đoạn thật chính xác (T06-075, T06-134, slide D1/8…) — grounding mạnh hơn fixture.
2. Nguồn SLIDE áp đảo T04 (slide ngắn-gọn-dễ-trích; T04 chỉ 7 segments) → cân nhắc tăng excerpt T04 lượt sau.
3. Cùng prompt 2 lần ra format khác nhau (T01 pass→fail) → golden set data thật phải chạy mỗi case ≥2 lượt.
4. Validator hiện tại quá khắt (đòi mã cả ở evidence) — lượt sau chấp nhận mã ở source HOẶC evidence.

**Kết luận:** pipeline chạy được trên data thật, 0 bịa. Số thấp hơn fixture là bình thường
(data nhiễu hơn) — phân tích này chính là nội dung pitch. Số CP3 nộp = lượt RAG;
lượt T06 là evidence “chạy được data thật” + hướng scale.
