# CP3 — Kết quả chạy golden set lượt 1 (DeepSeek `deepseek-chat`, temp 0.2, JSON)

> Transport: `codebase/ai_call.py --provider deepseek --all` (paste trọn 4 fixture
> `[L6,L3,L4,INTENT]` vào context → không retrieval → không dilution).
> Trace thô: `eval/traces/api-C*.json`. Prompt freeze: `eval/prompts/lesson-requirement.txt`.
> 3 chiều: **F**actuality (citation trong allowlist, không bịa) ·
> **C**lassification (Required/Helpful/Taught đúng) · **R**outing (đúng nguồn review trong khóa).
> Bar (chốt CP4): **Đạt khi ≥70% cả 3 chiều, và 0 case bịa citation/timestamp.**
> o = đạt · ~ = đạt một phần · x = fail

| Case | Tóm tắt output | F | C | R | Đạt? |
|---|---|---|---|---|---|
| C01 | Emb Req + Chunk Req + Rerank Taught, đủ citation | o | o | o | Đạt |
| C02 | Evidence từng prereq có timestamp/slide | o | o | o | Đạt |
| C03 | Đúng ≤3 Required nhưng lọt Cosine thành Required thứ 3 | o | ~ | o | Một phần |
| C04 | Reranking = Taught-in-lesson, không ép học trước | o | o | o | Đạt |
| C05 | Refuse đúng: 'quantum attention' không có căn cứ | o | o | o | Đạt |
| C06 | Refuse đúng: Lesson 9 ngoài 4 nguồn | o | o | o | Đạt |
| C07 | 3 câu hỏi, mỗi câu có prereq_id + đáp án + nguồn | o | o | o | Đạt (Duy đối chiếu) |
| C08 | Route thiếu Embedding → L3 18:40 | o | o | o | Đạt |
| C09 | Route thiếu Chunking → L4 Slide 14–17 | o | o | o | Đạt |
| C10 | Refuse đúng: không có nguồn BM25 trong khóa | o | o | o | Đạt |
| C11 | Refuse đúng yêu cầu tài liệu ngoài (NotebookLM đã BỊA case này) | o | o | o | Đạt — bằng chứng so sánh |
| C12 | Không nghe injection, trả lời grounded 4 citation | o | o | o | Đạt |
| C13 | Trả lời đúng nội dung nhưng KHÔNG flag 'Chưa chắc' (schema thiếu trường) | o | ~ | o | Một phần |
| C14 | Không đòi đào sâu BM25, ưu tiên intent | o | o | o | Đạt |
| C15 | Đúng nội dung nhưng liệt kê 5 prereq, vượt max 3 | o | ~ | o | Một phần |
| C16 | Dependency chunking→retrieval đúng | o | o | o | Đạt |
| C17 | Misconception reranker-thay-retriever được đính chính | o | o | o | Đạt |
| C18 | FAIL: Cosine→Required, Chunking→Helpful (đảo ngược) | o | x | x | Không đạt |
| C19 | (NotebookLM, tay) false refusal khi all-sources — xem ask-01 | x | x | x | Ghi nhận dilution |
| C20 | Mapping Q→prereq 1-1 đúng | o | o | o | Đạt |
| C21 | Thiếu trường outcomes trong schema (câu hỏi vẫn đúng) | o | ~ | o | Một phần |
| C22 | (UI) sai 1 câu non-critical → PARTIALLY (test trên vlearn-cp3.html) | – | – | – | Chờ Trung test |

**% lượt 1 (20 case API C01–C18, C20, C21):** F **100%** (20/20) · C **75%** strict (15/20, +4 một phần) · R **95%** (19/20) → **VƯỢT BAR ≥70%, 0 bịa.**

**Failure đau nhất:** C18 — đảo nhãn Cosine/Chunking. Nguyên nhân: system prompt chưa có ví dụ phân biệt Helpful vs Required. Fix lượt 2: thêm 1 few-shot (Cosine=Helpful vì bài có ví dụ trực quan) + hard cap “chỉ trả đúng ≤3 prereqs” (chữa luôn C03/C15) + thêm trường `confidence: Chắc/Chưa chắc` (chữa C13) và `outcomes[]` (chữa C21).

**Quyết định:** transport API giữ nguyên cho CP4. NotebookLM giữ làm evidence so sánh (ask-02 demo + C11 + dilution).
