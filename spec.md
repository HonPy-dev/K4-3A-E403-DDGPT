# AI SPEC — VLearn Ready: Lesson Prep trước khi học

Hướng: A — VLearn  
Loại: Tính năng mới  
Trạng thái CP4: **chốt phạm vi và quality bar ngày 17/09/2026**

## §1. User & Job

**Job executor:** học viên VLearn sắp bắt đầu một lesson mới, ở đây là Lesson 6 · RAG + Reranking.

**Workflow hiện tại:** mở lesson → gặp thuật ngữ/kiến thức ngầm định → dừng để tự tìm trong lesson trước hoặc web → quay lại lesson. Với nội dung có dependency, việc gián đoạn làm người học mất mạch theo bài.

**Core JTBD:** Trước khi bắt đầu một lesson, học viên muốn biết kiến thức nào cần ôn và mở đúng phần trong khóa để theo bài không bị gián đoạn.

**Problem statement:** Học viên chưa biết lesson giả định kiến thức nền nào, khái niệm nào sẽ được dạy ngay trong bài, và nên xem lại đúng đoạn nào khi thiếu kiến thức.

**Evidence A — khảo sát 25 học viên:** 18/25 người (72%) xác nhận từng gặp pain thiếu kiến thức nền khi bắt đầu hoặc đang theo một buổi học. Nhóm bị ảnh hưởng báo cáo tình trạng xảy ra thường xuyên ở mỗi buổi và mất từ 30 phút trở lên cho mỗi lần tự tra cứu/ôn lại. Ở cận dưới, tác động tương đương ít nhất `18 × 30 = 540 phút`, tức **9 person-hours cho mỗi buổi học** trong nhóm người xác nhận pain. Tổng hợp tại `evidence/survey-summary.md`.

**Evidence B — mời 2 người ngoài nhóm dùng thử:**. Phạm vi đã kiểm: Lesson 6 target, Lesson 3, Lesson 4 và Instructor Intent. Mining xác nhận hai dependency không được định nghĩa lại trong Lesson 6 (embedding, chunking), một concept được dạy trong lesson (reranking), một dependency có hậu quả rõ và một misconception do giảng viên nêu.

**Kết luận evidence:** kết quả khảo sát cho thấy pain có độ phủ đáng kể; content mining cho thấy hệ thống có đủ dữ liệu Tier-1 để can thiệp bằng một lát cắt nhỏ, kiểm chứng được.

## §2. Impact & quyết định chọn

| Ý tưởng | Job phục vụ | Tín hiệu từ mining | Tần suất / chi phí với user | Khả thi trong hackathon | Quyết định |
|---|---|---|---|---|---|
| Lesson Preview | Biết lesson sắp học gì | 3 outcomes của L6 có sẵn | Pain chung: 18/25; chưa tách riêng nhu cầu preview | Cao, nhưng gần summarization | Loại: chưa xử lý dependency/routing |
| Prerequisite Prep | Biết cần chuẩn bị gì và xem ở đâu | 2 prerequisite không được dạy lại; 2 nguồn review rõ | Trực tiếp xử lý ≥30 phút tự tra cứu/lần của nhóm pain | Cao: nguồn Tier-1, classification, route | **Chọn** |
| Readiness Check cá nhân hóa | Biết bản thân đã đủ nền chưa | Có 3 câu quiz map với prerequisite | Có thể phát hiện gap, nhưng chi phí sai cao hơn | Trung bình: cần calibration theo người học | Không chọn làm AI decision chính; chỉ là lớp UI sau Prep |

**Ý tưởng chọn:** Prerequisite Prep. AI quyết định concept là `Required`, `Helpful` hay `Taught-in-lesson`, chỉ route khi có nguồn trong khóa.

**Tính toán impact cận dưới:** 72% người khảo sát xác nhận pain; với tối thiểu 30 phút/lần và tần suất mỗi buổi, nhóm có thể giảm một phần của ít nhất 9 person-hours/buổi trong mẫu khảo sát nếu route đúng nguồn ngay trước lesson. Đây là cận dưới từ số liệu tự báo cáo, chưa phải causal impact của prototype.

## §3. Giải pháp tương tự đã nghiên cứu

| Sản phẩm / tài liệu so sánh | Điều đã quan sát trong artifact | Điều áp dụng / tránh |
|---|---|---|
| NotebookLM | Trace `eval/traces/ask-02-targeted-pass.json` cho thấy output có citation khi giới hạn đúng 4 nguồn; case C11 ghi nhận rủi ro bịa BM25 khi yêu cầu ngoài phạm vi | Giới hạn Tier-1, validate source allowlist, từ chối có redirect |
| VLearn Tutor hiện có | Reader có flow học và nút mở Ready | Đặt Prep trước lesson, không biến nó thành chatbot chung |
| ChatGPT Study Mode / Khanmigo | Đã rà tài liệu sản phẩm chính thức; log tại `evidence/competitive-research.md` | Học flow Socratic, knowledge checks, grounding vào content library; VLearn Ready khác ở bước prep ngắn và citation allowlist |

## §4. Thiết kế

**Lát cắt một câu:** Trước khi học viên bắt đầu Lesson 6, AI đọc nguồn Tier-1 để phân loại tối đa ba concept là Required/Helpful/Taught-in-lesson và route học viên thiếu nền tới đúng đoạn review trong khóa.

**Input:** 4 nguồn đã allowlist (`L6`, `L3`, `L4`, `INTENT`).  
**Output:** outcomes, prerequisite có evidence/citation, route review, 3 readiness questions và verdict sau quiz.  
**AI decision trung tâm:** phân loại prerequisite và chọn nguồn route.  
**Phần AI thật:** `server.py` gọi DeepSeek, ép JSON, validate citation/format, lưu trace vào `eval/traces/`.  
**Phần mock:** lesson chưa có fixture và fallback khi mất mạng/hết key. UI hiển thị banner phân biệt rõ mock/fallback/live.

**Non-goals:**

1. Không tìm web tự do hoặc tự tạo link/timestamp ngoài nguồn khóa học.
2. Không chẩn đoán năng lực dài hạn hay cá nhân hóa lộ trình toàn khóa.
3. Không thay thế nội dung bài giảng hoặc ép học viên phải ôn trước khi vào lesson.
4. Không tạo video intro AI hay chatbot trả lời mọi chủ đề.

**Automation:** conditional. Với evidence có allowlist và output vượt validation, hệ thống tự tạo Prep. Thiếu căn cứ, lesson ngoài fixture hoặc API lỗi thì thu hẹp phạm vi/fallback. Sai prerequisite có thể làm học viên chuẩn bị thừa hoặc thiếu nền, vì vậy không dùng automate không điều kiện.

### §4b. Nguyên tắc HAX/PAIR đã áp dụng

| Nguyên tắc | Áp cụ thể trong prototype |
|---|---|
| G1 — làm rõ hệ thống làm được gì | Nút và banner nói rõ `AI live`, `mock` hoặc `fallback`; Lesson 6/T06 là hai lesson có fixture live. |
| G2 — làm rõ hệ thống làm tốt đến đâu | Card hiển thị evidence/source; API trả `trace` để kiểm tra; chỉ claim grounded trong allowlist. |
| G10 — thu hẹp phạm vi khi nghi ngờ | C05/C06/C10/C11 yêu cầu output “chưa đủ căn cứ” hoặc từ chối mềm; server chỉ cho phép source trong registry. |
| G8 — dễ gạt bỏ | `Bỏ qua & Vào học ngay` luôn có; Prep không khóa lesson. |
| G9 — sửa/dùng lại dễ dàng | `Kiểm tra lại` và `Làm lại kiểm tra` đưa người học quay về quiz. |
| G11 — giải thích vì sao | Mỗi prerequisite có evidence/source và route Lesson 3 18:40 hoặc Lesson 4 slide 14–17. |

## §5. Kiểu lỗi — bốn lớp chỗ khó và kịch bản

| Kịch bản | Lớp | Hành vi mong muốn | Case kiểm thử | Nguyên tắc |
|---|---|---|---|---|
| Concept không có trong nguồn: quantum attention | ① Nguồn sự thật | Loại, không định nghĩa/bịa citation | C05 | G10, G11 |
| Người học đòi route BM25 không có trong khóa | ① Nguồn sự thật | Nói không tìm thấy trong tài liệu, không tạo timestamp | C10 | G10 |
| Học viên nói mơ hồ “không chắc hiểu embedding” | ② Mơ hồ | Báo chưa chắc, hỏi thêm/thử quiz; không auto-fail | C13 | G10, G9 |
| Có quá nhiều concept trong lesson | ② Mơ hồ | Tối đa 3 Required, ưu tiên bằng evidence | C03 | G2 |
| Hỏi prerequisite cho Lesson 9 chưa có fixture | ③ Ngoài phạm vi | Nói chưa đủ nguồn, không tạo Prep | C06 | G1, G10 |
| Prompt injection yêu cầu bịa 5 prerequisite | ③ Ngoài phạm vi | Bỏ qua instruction xung đột, chỉ trả grounded output | C12 | G10 |
| Nhầm reranker thay retriever | ④ Đặc thù domain | Đính chính top-50 → top-5 với L6/Intent | C15, C17 | G11 |
| Chunking xấu dù reranker tốt | ④ Đặc thù domain | Nêu dependency và route về L4 | C16 | G11 |
| Reranking được dạy trong bài nhưng bị ép học trước | ④ Đặc thù domain | Gắn `Taught-in-lesson`, không tạo prep bắt buộc | C04 | G8, G11 |
| Cosine bị phân loại Required thay Helpful | ④ Đặc thù domain | Ghi fail, không che; sửa prompt/eval sau CP4 mà không đổi bar | C18 | G2, G11 |

## §6. Bốn đường đi của trải nghiệm

| Đường đi | Trigger | Hệ thống hiển thị | Hành động tiếp theo của user |
|---|---|---|---|
| Happy path | AI trả JSON hợp lệ, citation trong allowlist | Banner `Prep AI LIVE`, outcomes, labels và route | Làm 3 câu quiz hoặc vào bài ngay |
| Low-confidence | Input mơ hồ / evidence chưa đủ | `Chưa chắc` hoặc không recommend, hỏi thêm qua quiz | Xem nguồn/kiểm tra lại/skip |
| Failure / không căn cứ | Case không có nguồn, API lỗi/hết key | Từ chối có giới hạn hoặc banner fallback vàng | Dùng Prep cache đã validate hoặc vào bài |
| Correction | Học viên sai quiz hoặc không đồng ý verdict | PARTIALLY/NOT READY, mục ôn nhanh và nút làm lại | Mở đúng Lesson 3/Lesson 4, làm lại hoặc bỏ qua |

## §7. Kiểm thử

**Ba chiều chất lượng:**

| Chiều | Pass khi |
|---|---|
| Factuality (F) | Mọi citation/source nằm trong allowlist, không bịa source hoặc timestamp. |
| Classification (C) | Label Required/Helpful/Taught-in-lesson khớp expected của case; không vượt 3 Required. |
| Routing (R) | Khi cần ôn, route tới đúng source/đoạn trong khóa; không tạo link/route ngoài phạm vi. |

**Golden set:** `eval/tests.csv` gồm 22 case; 20 case API là lượt đo chính, C19 là dilution observation và C22 là UI deterministic. Các case phủ source truth, ambiguity, out-of-scope, domain risk, classification, robustness, question format và outcomes.

**Quality bar đã khóa:** **Đạt khi F ≥70%, C ≥70%, R ≥70% trên đủ 20 case API của một lượt đo, và 0 case bịa citation/timestamp.** Không sửa bar sau CP4.

| Lượt | Transport | F | C | R | So với bar | Failure đáng chú ý |
|---|---|---:|---:|---:|---|---|
| 1 | `ai_call.py --provider deepseek --all` | 100% | 75% | 95% | Đạt | C18 đảo Cosine/Chunking; C03/C13/C15/C21 một phần |
| 2 | DeepSeek, prompt siết format quiz | 100% | 80% | 95% | Đạt | C18 vẫn fail ổn định; C13/C21 còn một phần |
| Live CP4 | `server.py` → `/api/ask`, 20 case | 100% | 80% | 100% | Đạt | C03, C11, C13, C21 fail strict; C18 đã pass |

**Quy tắc chấm:** `o` = pass hoàn toàn, `~` = đúng một phần nhưng không tính pass strict cho C/R, `x` = fail. Mọi case và fail phải giữ trong báo cáo.

## §8. Phân công & kế hoạch

| Mảng | Người phụ trách | Việc CP4/CP5 |
|---|---|---|
| Evidence / mining | Đinh Mạnh Dũng — 2A202602975 | Xác nhận log mining, lưu bảng khảo sát và mã hóa chủ đề |
| Spec / impact | Nguyễn Hồng Phi — 2A202602750 (Trưởng nhóm) | Rà soát bảng impact, điều phối và freeze spec |
| Prompt / grounding | Trần Nguyễn Thái Duy — 2A202602991 | Kiểm tra prompt, allowlist, chạy 20 case live và lưu trace |
| Code / UI | Phạm Thành Trung — 2A202602949 | Hoàn thiện UI, kiểm tra Prep → Quiz → Review → Lesson |
| Evaluation / demo | Từ Hoàng Giang — 2A202602363 | Chấm case khó, tổng hợp F/C/R và quay video dự phòng |

**Willing users:** chọn ít nhất 2 người trong mẫu khảo sát đồng ý thử prototype trước CP5; lưu mã ẩn danh, feedback nguyên văn và changelog tại `validation/`.

**Kế hoạch LEC 6 / LAB 6:**

1. Trước LEC 6: người Prompt xác nhận `/api/health` có `key_present: true`; người Demo dry-run Lesson 6 và T06.
2. Trong LAB 6: chạy 20 case live; hai người chấm độc lập C03, C05, C10, C13, C18; ghi F/C/R và bất đồng.
3. Sau LAB 6: cập nhật `eval/results-run-live.md`, tạo `eval/metrics.json`, quay demo dự phòng; không đổi quality bar.

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| CP2 | Dựng Lesson Prep drawer + quiz flow | Kiểm chứng flow bấm được |
| CP3 lượt 1 | Thêm DeepSeek JSON, allowlist, 20-case API run | Cần AI thật, trace và baseline đo |
| CP3 lượt 2 | Siết rule 3–5 câu, 3 options, prerequisite mapping | C07/C15 format cần cải thiện |
| CP4 | Khóa bar F/C/R ≥70% và 0 bịa citation/timestamp | Giữ chuẩn “đạt” cố định trước CP5/CP6 |
| CP4 · C18 | Bổ sung tiêu chí dependency và boundary example vào system prompt | C18 fail ổn định do model nhầm Helpful với Required |

## Tự khai phần chưa hoàn thành tại CP4

1. Log competitive research đã hoàn tất ở mức desk research; chưa claim phiên dùng thử Khanmigo có đăng nhập.
2. Lượt live đã hoàn tất 20 case; bốn case C03/C11/C13/C21 chưa đạt strict và đã có failure analysis.
3. C18 đã được xác nhận pass ở lượt live; giữ trace fail cũ và trace pass mới làm bằng chứng before/after.
