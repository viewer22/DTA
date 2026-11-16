# Khung thuyết trình DTA301 (chia phần cho nhóm soạn)

Slide dùng: `reports/final_v2/DTA301_Final_Slides.pptx` (10 slide). Tổng thời gian nói khoảng **9–10 phút**, sau đó Q&A.
Mỗi người soạn lời nói cho phần mình theo khung dưới, viết vào chỗ "Lời nói", rồi gửi lại để ghép.

**Khung này bám theo đâu**
- *Slide mẫu của môn (template RBL 10 slide)*: đủ 10 mục Tên đề tài → Bối cảnh, RQ → Dataset → Làm sạch + 3 insight EDA → Mô hình, thiết kế thí nghiệm → Kết quả → Thảo luận, ca lỗi → Kết luận, hạn chế → GitHub, khai báo AI, Q&A. Bản slide final_v2 gộp Bối cảnh và RQ vào slide 2 và đặt GitHub, AI vào slide 10, nên vẫn đủ 10 mục. Template dặn: mỗi hình phải nói "hình cho thấy gì, liên quan RQ thế nào", không chụp code, mạch nói vấn đề → bằng chứng → phương pháp → kết quả → ý nghĩa.
- *Góp ý của cô (mail ngày 12/11)*: từng ý "khi present" của cô cho slide 1–10 được ghi thành mục **Cô yêu cầu giải thích** ở mỗi slide bên dưới. Cô nhấn mạnh hai điều cho cả bài:
  1. Làm nổi bật mạch **EDA → Feature Engineering → Model Development → Model Training → Model Evaluation → Model Selection** (slide 4 → 7, xem bảng dưới).
  2. **Decision Support chỉ là minh họa, không chiếm nhiều thời gian**: slide 8 tối đa 1 phút.

| Bước cô muốn thấy | Slide | Người nói |
|---|---|---|
| EDA | 4 | Thành |
| Feature Engineering (thêm v², bỏ biến rò rỉ) | 4–5 | Thành → Quyền |
| Model Development (công thức M1, baseline, đối chứng) | 5 | Quyền |
| Model Training (OLS, CV 5-fold × 10) | 5 | Quyền |
| Model Evaluation (MAE, Actual vs Predicted, R6, ngoại suy) | 6–7 | Đức Duy |
| Model Selection (vì sao M1, không phải GB) | 6 | Đức Duy |

**Quy tắc chung khi soạn**
- Mạch nói mỗi slide: hình này cho thấy gì → liên quan tới câu hỏi nghiên cứu thế nào → chuyển sang slide sau.
- Chỉ dùng số trong paper final_v2 (bảng số ở cuối file). Không dùng số cũ "Ridge thắng", "MAE 0,66".
- Không nói "an toàn", "đảm bảo bay được". Phần quyết định luôn nói là "kịch bản bán mô phỏng, so sánh tương đối".
- Slide 9–10 **không đọc lại số** của slide 6–8 (cô dặn), chỉ nói ý chính.
- Mỗi slide có 1 câu chốt, nói chậm.
- Cuối phần mình có 1 câu chuyển cho người sau.

---

## Phân công (5 người)

| Phần | Slide | Nội dung | Thời gian | Người trình bày |
|---|---|---|---|---|
| 1 | 1–2 | Mở đầu, giới thiệu nhóm, vấn đề và câu hỏi nghiên cứu | 1 phút 30 | **Duy PM** |
| 2 | 3–4 | Dữ liệu, cách tính năng lượng, chống rò rỉ, EDA | 2 phút | **Thành** |
| 3 | 5 | Phương pháp chính M1, training, cross-validation | 1 phút 45 | **Quyền** |
| 4 | 6–7 | So sánh mô hình, chọn M1, đánh giá M1 (R6, ngoại suy) | 2 phút 15 | **Đức Duy** |
| 5 | 8–10 | Lớp quyết định (≤ 1 phút), thảo luận, kết luận | 2 phút 30 | **Phát** |
| Q&A | | Câu hỏi phần nào thì người phần đó trả lời trước, Duy PM điều phối | | Cả nhóm |

Tổng khoảng 10 phút. Slide 5 là phần cô bảo cần tập trung nhất nên Quyền nói riêng một slide.

---

## PHẦN 1 · Slide 1–2 · Duy PM (1 phút 30)

### Slide 1 · Tên đề tài (30 giây)
Phải có:
- Chào hội đồng, tên đề tài, giới thiệu 5 thành viên và ai trình bày phần nào (Thành: dữ liệu, EDA; Quyền: phương pháp; Đức Duy: kết quả; Phát: quyết định, kết luận)
- Câu hỏi một dòng: trước khi bay, chỉ biết tốc độ, tải, độ cao cài đặt, chuyến này tốn bao nhiêu Wh?
- Dữ liệu bay thật của CMU, drone DJI Matrice 100

Cô yêu cầu: thông điệp ngắn, làm nổi bật mục tiêu dự đoán năng lượng trước chuyến bay; không nói kết quả an toàn bay như đã kiểm chứng.

Câu chốt: *"Chuyến này sẽ tốn bao nhiêu Wh?"*

Lời nói: ……………………………………………

### Slide 2 · Vấn đề và câu hỏi nghiên cứu (1 phút)
Phải có:
- Vấn đề: ngưỡng % pin cố định không biết chuyến nặng/nhẹ, nhanh/chậm, cao/thấp
- Việc chính: bài toán hồi quy, đầu ra là năng lượng (Wh), đo bằng MAE, RMSE, R²
- Việc phụ: ứng dụng FLY / CONDITIONAL / NO-FLY trên kịch bản bán mô phỏng
- Vì sao bán mô phỏng: dữ liệu không có SoC, SoH

Cô yêu cầu giải thích: vấn đề nghiên cứu, mục tiêu đề tài, và **phân biệt Energy Prediction với phần ứng dụng hỗ trợ quyết định**.

Câu chốt: *"Nhóm không kết luận về an toàn bay thật."*

Lời nói: ……………………………………………

Chuyển: "Để trả lời câu hỏi này, trước hết bạn Thành sẽ trình bày dữ liệu và cách nhóm tính năng lượng."

---

## PHẦN 2 · Slide 3–4 · Thành (2 phút)

### Slide 3 · Dữ liệu (1 phút)
Phải có:
- 257.896 dòng telemetry, 209 bản ghi, giữ 192 chuyến (13,0–37,7 Wh, trung bình 21,3 Wh)
- Tự tính năng lượng: P = V × I, tích phân hình thang theo thời gian, chia 3600; 3 cách tính lệch < 0,25%
- Loại 17 bản ghi theo 4 luật có nhật ký (speed = 0, đổi độ cao giữa chừng, tải 750 g, ghi dư sau hạ cánh)
- Chống rò rỉ: không dùng thời lượng bay (r = 0,83) vì chỉ biết sau khi bay; chia train/test theo chuyến
- Hạn chế: 180/192 chuyến cùng tuyến R1 ≈ 472 m

Cô yêu cầu giải thích: **vì sao giữ 192 chuyến**, **cách tính target Energy (Wh) từ telemetry**, **cách tránh Data Leakage**. Không cần đọc hết luật lọc.

Câu chốt: *"Thời lượng bay chỉ biết sau khi bay, dùng là rò rỉ dữ liệu."*

Lời nói: ……………………………………………

### Slide 4 · EDA (1 phút)
Phải có:
- Cách đọc hình: mỗi chấm là một chuyến, đường cam là trung bình mỗi mức
- Tải 0 → 500 g: 19,2 → 23,1 Wh, gần tuyến tính
- Độ cao +25 m ≈ +2,6 Wh, gần tuyến tính
- Tốc độ 4 → 10 m/s: 27,0 → 18,6 Wh rồi chững; drone thực tế chỉ đạt ≈ 10,7 m/s
- Cả 3 biến có ý nghĩa (p < 0,001)

Cô yêu cầu giải thích: không chỉ mô tả tăng/giảm mà nói **ý nghĩa** của kết quả EDA, đặc biệt **vì sao quan hệ Speed–Energy dẫn tới thêm speed²** (đây là bước EDA → Feature Engineering). Nói rõ hình dùng chung với Hình 2 của paper, cùng số liệu.

Câu chốt: *"Đường thẳng không mô tả được dạng cong của tốc độ, nên nhóm thêm v²."*

Lời nói: ……………………………………………

Chuyển: "Từ dạng cong của tốc độ, bạn Quyền sẽ trình bày mô hình chính của nhóm."

---

## PHẦN 3 · Slide 5 · Quyền (1 phút 45)

### Slide 5 · Phương pháp chính M1 (1 phút 45)
Phải có:
- Quy trình: Input → Feature engineering (thêm v², bỏ biến rò rỉ) → Training (OLS) → Evaluation → Prediction
- Công thức: Ê = 32,20 − 4,194v + 0,197v² + 0,0081m + 0,105h
- Đọc hệ số: +100 g → +0,81 Wh; +25 m → +2,62 Wh; đáy parabol ở 10,65 m/s
- Vì sao thêm v²: EDA + phần dư hồi quy tuyến tính hình chữ U theo tốc độ
- Không có siêu tham số, nghiệm đóng
- Đánh giá: 5-fold × 10 lần, seed 301, mọi mô hình dùng chung 50 cách chia
- Mô hình so sánh: baseline B0–B3, đối chứng RF và GB

- Câu tách bạch: "Slide này chỉ là mô hình dự đoán năng lượng; lớp quyết định là phần riêng ở slide 8."

Cô yêu cầu giải thích (cô ghi **đây là nội dung cần tập trung nhất**): các input features, nguyên lý hoạt động của M1, cách training, Cross-Validation, và phân biệt Energy Prediction với Decision Layer. Phần 2 nên dành nhiều thời gian nhất cho slide này.

Câu chốt: *"5 hệ số, đọc được bằng đơn vị vật lý."*

Lời nói: ……………………………………………

Chuyển: "Vậy M1 có tốt hơn các mô hình khác không, bạn Đức Duy sẽ trình bày kết quả."

---

## PHẦN 4 · Slide 6–7 · Đức Duy (2 phút 15)

### Slide 6 · So sánh mô hình (1 phút)
Phải có:
- Đoán trung bình: MAE ≈ 4,0 Wh
- Tuyến tính = Ridge = 1,48 Wh (3 biến gần như trực giao, Ridge không có gì để co)
- M1: 0,85 Wh (−43%), RMSE 1,38, R² 0,91, thắng 50/50 lần chia, p < 10⁻¹¹
- GB 0,83 Wh nhưng p = 0,79, không khác biệt có ý nghĩa
- Lý do chọn M1: ngoại suy tốt hơn, 5 hệ số, không dò siêu tham số

Cô yêu cầu giải thích: **vì sao Linear Regression và Ridge gần bằng nhau**, **vì sao M1 giảm MAE 1,48 → 0,85 Wh**, **vì sao vẫn chọn M1 dù GB thấp hơn một chút** (Model Selection). Không cần đưa thêm bảng kiểm định.

Câu chốt: *"Chính xác ngang mô hình cây nhưng đơn giản và giải thích được."*

Lời nói: ……………………………………………

### Slide 7 · Khi nào M1 tốt, khi nào chưa (1 phút 15)
Phải có:
- Hình trái (Actual vs Predicted): R1–R5 sát đường chéo, 97% chuyến sai ≤ 2 Wh
- R6 (≈ 837 m, gấp đôi R1): mọi mô hình đoán thiếu 19–48% vì không có biến cự ly
- Thêm cự ly thử: MAE R6 6,7 → 3,4 Wh, nhưng chỉ 5 chuyến nên là thăm dò
- Hình phải (ngoại suy): bỏ hẳn một mức khỏi train; cây sai 2,5–5 Wh, M1 sai 0,8–1,7 Wh
- Điểm yếu: M1 kém hơn khi bỏ 12 m/s (parabol đi lên, thực tế chững)

Cô yêu cầu giải thích: M1 **tốt hơn ở trường hợp nào, chưa tốt ở trường hợp nào và vì sao**; **nguyên nhân sai số lớn ở R6** và **hạn chế khi không dùng Distance làm feature**.

Câu chốt: *"R6 sai do thiếu cự ly trong dữ liệu, không phải do chọn sai mô hình."*

Lời nói: ……………………………………………

Chuyển: "Từ dự đoán năng lượng, nhóm thử một ứng dụng hỗ trợ quyết định, bạn Phát sẽ trình bày và kết luận."

---

## PHẦN 5 · Slide 8–10 · Phát (2 phút 30)

### Slide 8 · Lớp hỗ trợ quyết định (tối đa 1 phút, chỉ là minh họa)
Phải có:
- 4.800 kịch bản: năng lượng cần là đo thật, trạng thái pin là giả định
- Cận trên = Ê × q90 (q90 ≈ 1,05, tính chỉ trên tập train)
- FLY khi pin dùng được ≥ 1,2 × cận trên; CONDITIONAL 1,0–1,2; NO-FLY < 1,0
- Ngưỡng SoC cố định phải đánh đổi: 30% → false-safe 53,9%; 60% → hủy nhầm 23,1%
- Định nghĩa chỉ số: false-safe = không đủ pin mà vẫn cho FLY; hủy nhầm = đủ pin mà bị NO-FLY
- Ý nghĩa 3 trạng thái: FLY đủ cả dự trữ; CONDITIONAL vừa đủ nhưng thiếu dự trữ, chỉ bay khi thay pin, giảm tải hoặc người vận hành duyệt; NO-FLY không đủ
- Luật theo M1: false-safe 0,6%; hủy nhầm 13,6% → 3,0% nhờ 310 ca sang CONDITIONAL
- Vì sao **chưa chứng minh được số chuyến hủy thực tế giảm**: CONDITIONAL chưa phải bay thành công, và trạng thái pin là giả định

Cô yêu cầu giải thích: ý nghĩa các chỉ số, khác biệt FLY / CONDITIONAL / NO-FLY, vì sao kết quả chưa chứng minh giảm hủy thực tế; ghi rõ 4.800 kịch bản bán mô phỏng.

Câu chốt: *"CONDITIONAL không có nghĩa là bay thành công; đây là so sánh tương đối."*

Lời nói: ……………………………………………

### Slide 9 · Thảo luận (40 giây)
Phải có:
- Ý nghĩa thực tế: với drone và tuyến giống dữ liệu, có thể thay câu hỏi "pin còn bao nhiêu %" bằng "chuyến này cần bao nhiêu Wh"
- Vì sao ưu tiên M1: đơn giản, giải thích được, ổn định khi gặp cấu hình mới
- So với tài liệu: mô hình vật lý cần nhiều tham số giả định; ở đây hệ số ước lượng từ năng lượng đo thật, dạng cong theo tốc độ khớp định tính với mô hình công suất có xét tốc độ
- Chưa nên dùng khi: tuyến khác R1, drone khác, gió mạnh, ngoài dải 4–12 m/s hoặc 0–500 g, quyết định an toàn thật

Cô yêu cầu: không lặp lại chỉ số slide 6–8; giải thích ý nghĩa thực tế, vì sao ưu tiên M1, và điều kiện mô hình chưa áp dụng đáng tin cậy.

Câu chốt: *"Dùng được cho drone và tuyến giống dữ liệu, chưa dùng ngoài phạm vi đó."*

Lời nói: ……………………………………………

### Slide 10 · Kết luận (50 giây)
Phải có:
- Đã giải quyết: dự đoán năng lượng trước khi cất cánh từ 3 thông số, trên dữ liệu bay thật
- Đóng góp: M1 đề xuất từ EDA, so sánh công bằng 7 mô hình, quy trình tái lập được
- Hạn chế: một loại drone, gần như một tuyến, chưa có cự ly và gió, quyết định mới là bán mô phỏng
- Hướng tiếp: thu dữ liệu nhiều cự ly và gió, thử tương tác, kiểm chứng drone khác
- GitHub github.com/viewer22/dta, notebook 01 → 06, seed 301; khai báo dùng AI
- Cảm ơn, mời hội đồng đặt câu hỏi

Cô yêu cầu: tổng kết ngắn **đã giải quyết vấn đề gì, kết quả có ý nghĩa gì, hướng phát triển tiếp theo**; làm nổi bật phương pháp chọn, đóng góp chính, hạn chế quan trọng nhất. Không đọc lại số.

Lời nói: ……………………………………………

---

## Q&A: mỗi người chuẩn bị trước

- 3 câu hỏi khó nhất về phần mình và câu trả lời (xem gợi ý trong `Kich_ban_thuyet_trinh_va_QA.md`)
- 1 câu: "Em làm phần ……, và kiểm chéo phần ……"
- Không biết thì nói: "Phần này nhóm chưa kiểm tra, em xin ghi nhận." Không đoán số.

Số câu trong cột cuối là số thứ tự câu hỏi trong `Kich_ban_thuyet_trinh_va_QA.md`, mỗi người đọc kỹ các câu đó.

| Người | Phần làm | Kiểm chéo phần của | Câu hỏi phải trả lời được |
|---|---|---|---|
| Duy PM | Slide 1–2, điều phối Q&A | Phát (slide 8–10) | 1, 4, 27, 28, 29, 30 |
| Thành | Slide 3–4 | Quyền (slide 5) | 2, 3, 5, 6, 10 |
| Quyền | Slide 5 | Đức Duy (slide 6–7) | 7, 8, 9, 12, 13, 14, 15 |
| Đức Duy | Slide 6–7 | Thành (slide 3–4) | 11, 16, 17, 18, 19 |
| Phát | Slide 8–10 | Duy PM (slide 1–2) | 20, 21, 22, 23, 24, 25, 26 |

Ai cũng phải trả lời được câu 31 ("Em làm phần nào?") bằng một câu: "Em làm phần ……, và kiểm chéo phần của bạn ……".

---

## Bảng số liệu dùng chung (chỉ dùng số này)

| Mục | Số |
|---|---|
| Dữ liệu | 257.896 dòng · 209 bản ghi · giữ 192 chuyến · 13,0–37,7 Wh, tb 21,3 Wh |
| M1 | MAE 0,85 Wh · RMSE 1,38 · R² 0,91 · −43% so với tuyến tính 1,48 |
| Đối chứng | RF 0,88 · GB 0,83 (p = 0,79) · đoán trung bình 3,98 |
| Hệ số | 0,81 Wh/100 g · 2,62 Wh/25 m · v_opt 10,65 m/s |
| R6 | ≈ 837 m · MAE 6,7 Wh · + cự ly → 3,4 Wh (5 chuyến, thăm dò) |
| Ngoại suy | cây 2,5–5 Wh · M1 0,8–1,7 Wh · M1 thua ở 12 m/s (1,71 vs 0,78) |
| Quyết định | 4.800 kịch bản · q90 ≈ 1,05 · dự trữ 1,2 · false-safe 0,6% · hủy nhầm 13,6% → 3,0% |
| SoC cố định | 30%: false-safe 53,9% · 60%: hủy nhầm 23,1% |
