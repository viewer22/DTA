# Kịch bản thuyết trình DTA301 và bộ câu hỏi hội đồng

Dùng cùng `DTA301_Final_Slides.pptx` (bản final_v2, 10 slide). Mọi con số lấy từ `D5_Final_Paper` bản final_v2.
Tổng thời gian nói khoảng **9 phút**. Chữ **in đậm** là câu chốt, nói chậm và nhìn hội đồng.

---

## 0. Việc cần làm ngay trước khi lên

1. **Điền slide 1**: tên nhóm, lớp, thành viên, GVHD vẫn đang là "……". Paper cũng vậy.
2. Mở sẵn: slide (pdf dự phòng), paper pdf, repo `github.com/viewer22/dta`, notebook 06 đã chạy sẵn output (phòng khi bị yêu cầu demo).
3. **Bỏ số cũ khỏi đầu.** File `notes/yeu-cau-bao-ve-hoi-dong.md` có số cũ ("Ridge thắng RF", "MAE 0,66 Wh", "sai số 3%"). Bản bảo vệ là: **M1 = hồi quy + v², MAE 0,85 Wh, R² 0,91**. Nếu lỡ nói số cũ là mâu thuẫn với paper.
4. Ba từ không được nói: "an toàn", "đảm bảo bay được", "độ tin cậy đã hiệu chuẩn". Nói "trên kịch bản bán mô phỏng", "so sánh tương đối".

---

## 1. Kịch bản nói theo slide

### Slide 1 · Mở đầu (30 giây)
"Em chào thầy cô. Nhóm em trình bày đề tài dự đoán năng lượng chuyến bay trước khi cất cánh cho drone giao hàng. Câu hỏi rất cụ thể: trước khi bay, chỉ biết tốc độ, tải và độ cao cài đặt, **chuyến này sẽ tốn bao nhiêu Wh?** Dữ liệu là dữ liệu bay thật công khai của Carnegie Mellon, drone DJI Matrice 100."

### Slide 2 · Vấn đề và RQ (1 phút)
"Hiện người vận hành thường dùng ngưỡng phần trăm pin cố định, ví dụ còn trên 50% thì bay. Ngưỡng đó không biết chuyến sắp bay nặng hay nhẹ, nhanh hay chậm. Nên nhóm tách hai việc.
Việc chính là **bài toán hồi quy**: dự đoán năng lượng, đánh giá bằng MAE, RMSE, R² trên năng lượng đo thật.
Việc phụ là ứng dụng minh hoạ: đưa dự đoán vào luật FLY, CONDITIONAL, NO-FLY. Phần này chạy trên kịch bản bán mô phỏng vì dữ liệu không có trạng thái pin, **nên nhóm không kết luận về an toàn bay thật**."

### Slide 3 · Dữ liệu (1 phút)
"Dữ liệu có 257.896 dòng telemetry của 209 bản ghi. Dữ liệu không có cột năng lượng, nhóm tự tính: công suất bằng V nhân I, tích phân hình thang theo thời gian thật, chia 3600 ra Wh; đối chiếu ba cách tính lệch dưới 0,25%.
Nhóm loại 17 bản ghi theo 4 luật có nhật ký: tốc độ bằng 0, đổi độ cao giữa chừng, tải 750 g ngoài thiết kế, ghi dư sau hạ cánh. Còn 192 chuyến, từ 13 đến 38 Wh.
Điểm quan trọng: thời lượng bay tương quan 0,83 với năng lượng nhưng **chỉ biết sau khi bay, nên dùng là rò rỉ dữ liệu**. Nhóm chỉ dùng ba thông số cài đặt, và chia train/test theo chuyến."

### Slide 4 · EDA (1 phút)
"Mỗi chấm là một chuyến, đường cam là trung bình mỗi mức. Tải và độ cao tăng gần tuyến tính: thêm 25 m tốn thêm khoảng 2,6 Wh.
Tốc độ thì khác: năng lượng giảm từ 27 xuống 18,6 Wh khi tăng từ 4 lên 10 m/s rồi chững lại, vì drone thực tế chỉ đạt khoảng 10,7 m/s. **Một đường thẳng không mô tả được dạng cong này, nên nhóm thêm đặc trưng bình phương tốc độ.** Đây là chỗ EDA dẫn thẳng tới mô hình."

### Slide 5 · Phương pháp M1 (1 phút 30)
"Mô hình chính M1 là hồi quy tuyến tính có thêm v². Công thức: Ê = 32,2 − 4,19v + 0,197v² + 0,0081m + 0,105h.
Đọc hệ số: thêm 100 g tải tốn thêm 0,81 Wh, thêm 25 m độ cao tốn 2,62 Wh, còn phần tốc độ là parabol có đáy ở 10,65 m/s, khớp với tốc độ thật lớn nhất drone đạt được.
M1 vẫn tuyến tính theo tham số nên huấn luyện bằng bình phương tối thiểu, có nghiệm đóng, **không có siêu tham số phải dò**.
Đánh giá: 5-fold lặp 10 lần, seed 301, mọi mô hình dùng chung 50 cách chia. So sánh với 4 baseline và 2 mô hình đối chứng là Random Forest, Gradient Boosting."

### Slide 6 · So sánh mô hình (1 phút)
"Đoán trung bình sai khoảng 4 Wh. Hồi quy tuyến tính và Ridge cùng 1,48 Wh, vì thiết kế thí nghiệm làm ba biến gần như không tương quan, Ridge không có gì để co.
**M1 giảm MAE xuống 0,85 Wh, tức giảm 43%, R² 0,91, thắng ở 50 trên 50 lần chia.**
Gradient Boosting thấp hơn 0,02 Wh nhưng p bằng 0,79, không có ý nghĩa thống kê. Khi chính xác ngang nhau, nhóm chọn M1 vì ngoại suy tốt hơn, chỉ 5 hệ số và đọc được."

### Slide 7 · Khi nào M1 tốt, khi nào chưa (1 phút 15)
"Bên trái: tuyến R1 đến R5 nằm sát đường chéo, 97% chuyến sai không quá 2 Wh. Năm tam giác đỏ là tuyến R6 dài khoảng 837 m, gần gấp đôi R1; mọi mô hình đều đoán thiếu 19 đến 48%, vì **đầu vào không có cự ly**, không phải do chọn sai mô hình. Thêm cự ly thử nghiệm thì MAE R6 giảm từ 6,7 xuống 3,4 Wh, nhưng chỉ 5 chuyến nên là thăm dò.
Bên phải: bỏ hẳn một mức khỏi tập train rồi dự đoán đúng mức đó. Mô hình cây sai 2,5 đến 5 Wh vì chỉ lặp lại giá trị vùng gần nhất. M1 tốt hơn ở 3 trên 4 trường hợp, và kém hơn khi bỏ 12 m/s vì parabol đi lên còn thực tế chững. Nhóm nói thẳng điểm yếu này."

### Slide 8 · Lớp quyết định (1 phút)
"Phần minh hoạ, em nói ngắn. 4.800 kịch bản: năng lượng cần là đo thật, trạng thái pin là giả định ngẫu nhiên.
Lấy dự đoán nhân q90 khoảng 1,05 để ra cận trên. Pin dùng được gấp 1,2 lần cận trên thì FLY, từ 1,0 đến 1,2 là CONDITIONAL, dưới 1,0 là NO-FLY.
Ngưỡng SoC cố định phải đánh đổi: 30% thì 54% ca thiếu pin vẫn cho bay, 60% thì hủy nhầm 23%. Luật dựa trên M1 có false-safe 0,6%.
Hủy nhầm giảm từ 13,6% xuống 3% là do 310 ca chuyển sang CONDITIONAL. **CONDITIONAL không có nghĩa là bay thành công**, và đây chỉ là so sánh tương đối giữa các luật."

### Slide 9 · Thảo luận (40 giây)
"Ý nghĩa thực tế: với drone và tuyến bay giống dữ liệu, có thể thay câu hỏi pin còn bao nhiêu phần trăm bằng câu hỏi chuyến này cần bao nhiêu Wh. Nhóm ưu tiên M1 vì đơn giản, giải thích được và ổn định khi gặp cấu hình mới. Mô hình chưa nên dùng khi tuyến khác R1, drone khác, gió mạnh, hoặc tốc độ, tải ngoài dải đã bay."

### Slide 10 · Kết luận (40 giây)
"Tóm lại, nhóm dự đoán được năng lượng chuyến bay trước khi cất cánh từ ba thông số, bằng một mô hình 5 hệ số đề xuất từ EDA, chính xác ngang mô hình cây nhưng ổn định và giải thích được hơn. Hạn chế lớn nhất là một loại drone, gần như một tuyến. Hướng tiếp theo là thu thêm dữ liệu nhiều cự ly và gió, rồi kiểm chứng trên drone khác. Mã nguồn chạy lại theo notebook 01 đến 06, seed 301. Em cảm ơn thầy cô, mời thầy cô đặt câu hỏi."

---

## 2. Câu hỏi hội đồng hay hỏi (trả lời 2–3 câu là đủ)

### Dữ liệu
**1. Vì sao chọn dataset CMU?**
Là dữ liệu bay thật công khai hiếm hoi có V, I, GPS đồng bộ, với tốc độ, tải, độ cao được thiết kế có kiểm soát (3 tải × 5 tốc độ × 4 độ cao). License CC BY 4.0, có DOI.

**2. Năng lượng tính thế nào? Sao biết tính đúng?**
E = Σ ½(Pⱼ + Pⱼ₊₁)·Δtⱼ / 3600, P = V·I, Δt là thời gian thật giữa hai mẫu. Nhóm đối chiếu 3 cách tính, lệch nhau dưới 0,25% (chi tiết ở D2/paper mục III).

**3. Loại 17 bản ghi có phải để kết quả đẹp hơn không?**
Không. Luật lọc dựa trên thiết kế thí nghiệm, không dựa trên sai số mô hình: 13 bản ghi speed = 0 là bay thử hoặc treo, 2 chuyến đổi độ cao giữa chừng, 1 chuyến tải 750 g chỉ có một lần, 1 chuyến ghi dư 2 phút sau hạ cánh. Có nhật ký loại trừ.

**4. Dữ liệu có SoC, SoH, nhiệt độ pin không?**
Không. Đó là lý do phần quyết định phải mô phỏng trạng thái pin, và nhóm chỉ coi đó là minh hoạ.

**5. Sao không dùng thời lượng bay, tương quan tới 0,83?**
Thời lượng chỉ biết sau khi bay. Bài toán là dự đoán trước khi cất cánh, nên dùng nó là rò rỉ dữ liệu. Công suất và vận tốc đo cũng bị loại vì cùng lý do.

**6. Chia train/test thế nào, có rò rỉ không?**
Mỗi chuyến là một dòng; chia theo chuyến, telemetry của một chuyến không bao giờ nằm ở cả train và test. Mỗi lượt train 153–154 chuyến, test 38–39 chuyến.

### Mô hình
**7. Vì sao thêm v² mà không dùng mô hình phức tạp hơn ngay từ đầu?**
EDA cho thấy năng lượng giảm rồi chững theo tốc độ, và phần dư của hồi quy tuyến tính có hình chữ U theo tốc độ. Thêm v² sửa đúng chỗ đó, giảm MAE 43%. Mô hình cây sau đó không vượt được có ý nghĩa.

**8. Thử bậc 3 hay tương tác chưa?**
Có. v³ không cải thiện có ý nghĩa (p = 0,12), nên bậc 2 là đủ. Thêm ba tương tác v·m, v·h, m·h giảm thêm 0,11 Wh (p < 0,001); nhóm ghi trung thực trong paper và để là hướng phát triển, vì muốn giữ mô hình đơn giản, đọc được.
*(Nếu hỏi tiếp "vậy sao không dùng?": cải thiện 0,11 Wh, khoảng 0,5% năng lượng trung bình, đổi lại thêm 3 hệ số khó giải thích và dễ quá khớp hơn khi ngoại suy. Nhóm chưa kiểm tra ngoại suy của biến thể này nên chưa đổi.)*

**9. Vì sao Linear Regression và Ridge ra y hệt nhau?**
Thiết kế thí nghiệm làm ba biến gần như trực giao, lại có 192 chuyến cho 3 hệ số, nên không có đa cộng tuyến. Phạt alpha = 1 gần như không thay đổi hệ số.

**10. Vì sao baseline chỉ cự ly không hơn đoán trung bình?**
180/192 chuyến cùng tuyến R1, cự ly gần như không đổi nên không mang thông tin.

**11. GB thấp hơn M1, sao lại chọn M1?**
Thấp hơn 0,02 Wh, khoảng 0,1% năng lượng trung bình, p = 0,79. Khi không khác biệt, nhóm chọn theo 3 tiêu chí còn lại: M1 ngoại suy tốt hơn ở 3/4 mép, có RMSE thấp hơn (1,38 so với 1,41), chỉ 5 hệ số có đơn vị, không dò siêu tham số.

**12. Hệ số có ý nghĩa vật lý không?**
Có. 100 g tải tốn thêm 0,81 Wh, 25 m độ cao tốn 2,62 Wh (khớp EDA), cực tiểu tốc độ 10,65 m/s khớp tốc độ thật lớn nhất drone đạt (~10,7). Mọi hệ số p < 0,001. Lưu ý: 10,65 m/s là đặc điểm của dữ liệu này, không phải tốc độ tối ưu vật lý phổ quát.

**13. Tính thử một chuyến?**
8 m/s, 250 g, 50 m: Ê = 32,196 − 33,555 + 12,600 + 2,025 + 5,248 ≈ **18,5 Wh**.

**14. Hyperparameter của RF, GB chọn thế nào? Có công bằng không?**
Bảng VIII của paper ghi GB chọn max_depth bằng nested CV (CV lồng trong tập train), RF 200 cây. Mọi mô hình dùng cùng 50 cách chia, seed 301, nên so sánh công bằng. *(Xem lại notebook 04 cho tham số chi tiết của RF trước khi lên.)*

### Thí nghiệm và đánh giá
**15. Vì sao t-test hiệu chỉnh Nadeau–Bengio, không phải t-test thường?**
Các tập train trong CV chồng lên nhau, các lượt không độc lập, nên t-test thường đánh giá thấp phương sai và cho p quá nhỏ. Nadeau–Bengio hiệu chỉnh phương sai theo tỉ lệ test/train.

**16. MAE 0,85 Wh là tốt hay chưa?**
Bằng khoảng 4% năng lượng trung bình 21,3 Wh và dưới 1% dung lượng pin 99,9 Wh. So với đoán trung bình (3,98 Wh) giảm hơn 4 lần.

**17. Sao R6 sai nhiều vậy? Có phải mô hình kém?**
Không phụ thuộc mô hình: cả 4 mô hình đều sai 6,7–7,0 Wh trên R6. Nguyên nhân là R6 dài gấp đôi R1 mà đầu vào không có cự ly. Thêm cự ly thử thì giảm còn 3,4 Wh, nhưng chỉ có 5 chuyến R6 nên chưa đủ tin cậy. Kết luận: M1 chỉ dùng cho tuyến giống R1.

**18. Phần dư có vấn đề gì không?**
Phần dư không tăng theo giá trị dự đoán (Spearman ρ = 0,005, p = 0,95), không lệch hệ thống ở R1–R5. Ngoại lệ duy nhất là R6.

**19. Thử ngoại suy làm thế nào?**
Bỏ hẳn một mức biên (4 m/s, 12 m/s, 25 m, 100 m) khỏi train rồi dự đoán đúng mức đó. Cây sai 2,5–5 Wh, M1 sai 0,8–1,7 Wh. M1 thua khi bỏ 12 m/s (1,71 so với 0,78 Wh của GB).
*Điểm cộng nên nói:* ba mép M1 thắng (bay chậm, thấp, cao) đều là cấu hình tốn năng lượng, tức chỗ đoán thiếu nguy hiểm hơn cho pin.

### Lớp quyết định
**20. Kịch bản bán mô phỏng là gì?**
Mỗi chuyến ghép 25 trạng thái pin ngẫu nhiên → 4.800 kịch bản. Năng lượng cần là đo thật. Pin dùng được E_avail = 99,9 · SoH · k(T) · (SoC − 0,2), với SoC ~ U(0,15; 1), SoH ~ U(0,7; 1), T ~ U(−10; 40) °C. "Không đủ pin" khi năng lượng thật > E_avail (38,7% kịch bản).

**21. q90 là gì, có rò rỉ không?**
Phân vị 90% của tỉ số năng lượng thật / dự đoán, tính bằng dự đoán out-of-fold **chỉ trong tập train** của mỗi lượt. Khoảng 1,042–1,053. Trên tập test, 92,2% chuyến không vượt cận trên.

**22. Vì sao hệ số dự trữ 1,2?**
Chọn trước theo quy ước dự trữ trong đề cương, không tối ưu trên dữ liệu. Đã thử 1,1 và 1,3: thứ tự giữa các luật không đổi.

**23. False-safe là gì, sao quan trọng hơn hủy nhầm?**
False-safe = ca không đủ pin mà vẫn cho FLY, có thể rơi máy. Hủy nhầm chỉ mất một chuyến giao. Nên ưu tiên giảm false-safe trước.

**24. Kết quả quyết định có ổn định không?**
Có kiểm tra độ nhạy: đổi dung lượng pin 129,96 Wh, dự trữ 1,1/1,3, SoC đọc sai ±5 điểm, seed 302–305. Q4 luôn có false-safe ≤ 0,8% và hủy nhầm ≤ 3,9%.

**25. 11 ca false-safe còn lại là gì?**
Đều thuộc tuyến R6, đúng ca lỗi đã phân tích ở slide 7. Nhất quán giữa hai phần.

**26. Nhãn quyết định có phải kết quả bay thật không? Có vòng lặp không?**
Không phải bay thật. Năng lượng cần là đo thật nên không vòng lặp ở phía nhu cầu, nhưng trạng thái pin là giả định nên con số chỉ so sánh tương đối giữa các luật, chưa chứng minh giảm số chuyến bị hủy thực tế.

### Tổng thể
**27. Hạn chế lớn nhất?**
Một loại drone, gần như một tuyến, không có cự ly và gió trong đầu vào, phần quyết định là bán mô phỏng. Không phải chứng nhận an toàn bay.

**28. Nếu làm tiếp sẽ làm gì?**
Thu dữ liệu nhiều cự ly, nhiều điều kiện gió để đưa cự ly kế hoạch và dự báo gió vào mô hình; đánh giá theo nhóm ngày bay hoặc tuyến; thử biến thể có tương tác; kiểm chứng trên drone khác có dữ liệu pin thật.

**29. Người khác chạy lại thế nào?**
Tải parameters.csv và flights.csv từ KiltHub vào `data/raw/`, cài `requirements.txt`, chạy notebook 01 → 06, seed 301. Kết quả ra ở `reports/`, hình `reports/figures/final_*.png` dùng chung cho paper và slide.

**30. Dùng AI thế nào?**
Claude hỗ trợ giải thích khái niệm thống kê, gợi ý code, vẽ hình, biên tập. Nhóm tự chạy lại toàn bộ notebook, đối chiếu từng con số, kiểm tra tài liệu tham khảo. AI không tạo dữ liệu.

**31. Em làm phần nào?**
Mỗi người chuẩn bị trước 1 câu: phần mình làm + phần mình kiểm chéo.

---

## 3. Nếu bị hỏi câu không biết

Nói: "Phần này nhóm chưa kiểm tra, em xin ghi nhận và bổ sung." Đừng đoán số. Hội đồng đánh giá cao việc nói rõ giới hạn hơn là trả lời chắc mà sai.

## 4. Thẻ số liệu cần thuộc

| | |
|---|---|
| Dữ liệu | 257.896 dòng · 209 bản ghi · giữ 192 chuyến · 13,0–37,7 Wh, tb 21,3 Wh |
| M1 | MAE 0,85 Wh · RMSE 1,38 · R² 0,91 · −43% so với tuyến tính (1,48) |
| Đối chứng | RF 0,88 · GB 0,83 (p = 0,79) · đoán trung bình 3,98 |
| Hệ số | 0,81 Wh/100 g · 2,62 Wh/25 m · v_opt 10,65 m/s |
| R6 | ~837 m · MAE 6,7 Wh · + cự ly → 3,4 Wh (5 chuyến, thăm dò) |
| Ngoại suy | cây 2,5–5 Wh · M1 0,8–1,7 Wh · M1 thua ở 12 m/s (1,71 vs 0,78) |
| Quyết định | 4.800 kịch bản · q90 ≈ 1,05 · dự trữ 1,2 · false-safe 0,6% · hủy nhầm 13,6% → 3,0% (310 ca sang CONDITIONAL) |
| SoC cố định | 30%: false-safe 53,9% · 60%: hủy nhầm 23,1% |
