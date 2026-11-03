# Dự báo năng lượng tiêu thụ trước chuyến bay của UAV giao hàng từ các thông số lập kế hoạch

Nhóm đồ án DTA301  |  Trường Đại học FPT

### Tóm tắt

Nghiên cứu dự báo năng lượng chuyến bay drone từ tốc độ, tải trọng và độ cao cài đặt trước khi bay. Điện áp và dòng điện được tích phân hình thang theo khoảng lấy mẫu thực tế. Sau lọc, giữ lại 192 trong 209 chuyến. Hồi quy tuyến tính và Ridge được so sánh với hồi quy thêm bình phương tốc độ, Random Forest và Gradient Boosting. Kiểm định chéo năm phần lặp mười lần được áp dụng; siêu tham số cây được chọn trong tập huấn luyện từng lượt. Hồi quy thêm bình phương tốc độ đạt sai số tuyệt đối trung bình 0,849 Wh, căn sai số bình phương trung bình 1,375 Wh và hệ số xác định trung bình 0,908. Sai số tuyệt đối giảm 42,5% so với hồi quy tuyến tính. Gradient Boosting có sai số tuyệt đối thấp hơn nhẹ, nhưng kiểm định có hiệu chỉnh chưa phát hiện khác biệt có ý nghĩa thống kê. Hồi quy thêm bình phương tốc độ tốt nhất ở ba trong bốn thử nghiệm mức biên. Tất cả mô hình vẫn dự đoán thiếu năm chuyến R6 dài hơn, cho thấy hạn chế khi thiếu cự ly. Kết quả ủng hộ dự báo năng lượng dễ diễn giải trong điều kiện quan sát, chưa xác lập độ tin cậy trên tuyến mới hoặc khả năng quyết định cho phép bay.

Từ khóa: dự báo năng lượng UAV; lập kế hoạch trước bay; hồi quy đa thức; kiểm định chéo; drone giao hàng.

## I Giới thiệu

Drone giao hàng cần đủ năng lượng khả dụng để hoàn thành chuyến bay dự kiến. Dự báo trước khi cất cánh đòi hỏi phân biệt thông số kế hoạch với telemetry chỉ thu được trong lúc bay. Mô hình dùng thời gian bay thực tế hoặc công suất điện trung bình làm đầu vào có thể cho kết quả tốt nhưng không phù hợp ở thời điểm lập kế hoạch. Vì vậy, nghiên cứu xây dựng bài toán hồi quy ở cấp chuyến bay, với năng lượng tính bằng Wh là biến mục tiêu; tốc độ cài đặt, khối lượng hàng và độ cao cài đặt là ba biến dự báo chính.

Rodrigues và cộng sự công bố dữ liệu vị trí và điện của 209 chuyến bay DJI Matrice 100 [1], với dữ liệu gốc được lưu tại KiltHub [2]. Nghiên cứu tiếp theo xây dựng mô hình năng lượng dựa trên phân tích vật lý và dữ liệu thực nghiệm, đồng thời xem xét năng lượng và phát thải giao hàng [3]. Bài này sử dụng cùng nguồn dữ liệu công khai để so sánh hồi quy gọn nhẹ với các mô hình tổ hợp cây. Nghiên cứu không tái hiện mô hình vật lý của bài gốc và không so sánh trực tiếp độ chính xác vì cách chọn dữ liệu, đầu vào và quy trình đánh giá khác nhau.

Câu hỏi nghiên cứu là liệu bổ sung một thành phần phi tuyến đơn giản của tốc độ có cải thiện dự báo năng lượng mà vẫn dễ diễn giải hay không. Phân tích kết hợp cách tính nhãn năng lượng có thể kiểm tra, cách chia dữ liệu chung, chẩn đoán phần dư và thử nghiệm bỏ mức biên. Sai số theo tuyến được xem xét cùng độ chính xác tổng thể để tránh đồng nhất sai số trung bình thấp với độ tin cậy ở mọi chuyến.

## II Phương pháp nghiên cứu

### A Dữ liệu và lựa chọn chuyến bay

Dữ liệu cục bộ gồm parameters.csv có 209 dòng và 7 cột, cùng flights.csv có 257.896 dòng telemetry và 28 cột. Hai tệp chứa cùng 209 mã chuyến bay. Tệp tham số cung cấp thông số vận hành; tệp telemetry chứa thời gian, điện áp, dòng điện, vị trí, vận tốc và các phép đo khác. Phạm vi chính gồm tốc độ cài đặt 4–12 m/s, tải trọng 0–500 g và độ cao cài đặt 25–100 m. Ba mức tải được giữ lại là 0, 250 và 500 g, không phải năm mức cách đều.

BẢNG I  Các quy tắc loại trừ chuyến bay

| Quy tắc | Số chuyến loại | Lý do |
| --- | --- | --- |
| Đo tĩnh và bay treo | 13 | Tốc độ cài đặt bằng 0 |
| Thay đổi độ cao giữa chuyến | 2 | R7 không có một mức độ cao duy nhất |
| Tải ngoài phạm vi | 1 | Chỉ một chuyến chở 750 g |
| Ghi kéo dài sau hạ cánh | 1 | Chuyến 196 có đoạn chờ dài |
| Chuyến được giữ lại | 192 | 209 trừ 17 chuyến loại |

Đây là quy tắc chọn mẫu của nghiên cứu, không hàm ý mọi phép đo bị loại đều không hợp lệ. Riêng chuyến 196 được pipeline hiện tại loại bỏ thay vì cắt đoạn chờ. Vì vậy, phạm vi nhãn mục tiêu gắn với các bản ghi được giữ lại; ảnh hưởng của lựa chọn này cần được kiểm tra trong phân tích độ nhạy sau này. Hai tệp đầu vào không có giá trị thiếu hoặc dòng trùng. Độ cao được chuyển từ dạng chữ sang số sau khi loại chuyến thay đổi độ cao. Mỗi chuyến giữ lại đóng góp đúng một dòng dữ liệu mô hình.

### B Xây dựng biến mục tiêu năng lượng

Tại mẫu j của chuyến i, công suất điện là Pᵢⱼ = Vᵢⱼ Iᵢⱼ. Năng lượng được tích phân trên toàn bản ghi được giữ lại, sử dụng thời gian thực tế và quy tắc hình thang:

Eᵢ = (1/3600) ∑ⱼ₌₂ⁿᵢ [(Pᵢ,ⱼ₋₁ + Pᵢⱼ)/2] (tᵢⱼ − tᵢ,ⱼ₋₁)     (1)

Điện áp tính bằng V, dòng điện bằng A và thời gian bằng giây; chia 3600 để đổi J sang Wh. Khoảng lấy mẫu trung bình là 0,15025 s, dao động 0,06–5,28 s trên dữ liệu thô. Các khoảng đều dương nhưng không bằng nhau. Pipeline giữ nguyên dòng điện âm nhỏ và tích phân hình thang qua các khoảng gián đoạn được giữ lại, không tái tạo công suất thực sự chưa quan sát trong khoảng đó. So với tổng Riemann trái, độ lệch trung bình là 0,051% và lớn nhất 0,247% trên các chuyến giữ lại. Sự thống nhất giữa hai quy tắc là kiểm tra số học, không thay thế hiệu chuẩn cảm biến độc lập.

![energy_VI.png](work/assets/energy_VI.png)

Hình 1. Công suất điện của chuyến 1. Diện tích tích phân tương ứng 21,766 Wh.

### C Biến đầu vào và cấu hình mô hình

Vector đầu vào chính là x = [v, m, h], trong đó v là tốc độ ngang cài đặt tính bằng m/s, m là tải trọng tính bằng gram và h là độ cao cài đặt tính bằng mét. Đây là thông số kế hoạch, không phải giá trị trung bình đo trong chuyến bay. Thời gian ghi, công suất trung bình, công suất cực đại và vận tốc đo được không nằm trong ma trận dự báo. Gió telemetry cũng bị loại vì quy trình hiện tại chưa cung cấp dự báo thời tiết có sẵn ở thời điểm dự đoán. Trạng thái sạc và trạng thái sức khỏe pin không phải đầu vào của các mô hình đã triển khai.

BẢNG II  Cấu hình các mô hình đã triển khai

| Mô hình | Cấu hình |
| --- | --- |
| B0 Trung bình | Trung bình nhãn trong tập huấn luyện; không dùng đầu vào |
| B1 Cự ly | Hồi quy tuyến tính theo trung vị chiều dài GPS của tuyến |
| B2 Tuyến tính | Bình phương tối thiểu với v, m, h |
| B3 Ridge | v, m, h; alpha = 1; không chuẩn hóa thang đo |
| M1 Bình phương tốc độ | Bình phương tối thiểu với v, m, h, v² |
| M2 Random Forest | 200 cây; min_samples_leaf thuộc {1, 3, 5} |
| M3 Gradient Boosting | 200 bước; learning_rate = 0,05; max_depth thuộc {1, 2, 3} |

Mô hình B2 cộng cự ly là thí nghiệm thăm dò. Cự ly được dựng lại bằng tổng các đoạn GPS ngang và gán cho mỗi tuyến trung vị chiều dài đường đã ghi. Đây là đại diện tuyến từ dữ liệu quan sát, tính trước khi chia tập, không phải hình học nhiệm vụ được cung cấp độc lập. Cự ly không tham gia so sánh chính M1–M3. Các bộ ước lượng dùng scikit-learn [4]; tham số không liệt kê trong Bảng II giữ giá trị mặc định của phiên bản triển khai.

### D Kiểm định chéo và chỉ số đánh giá

RepeatedKFold sử dụng năm phần, mười lần lặp và random_state = 301 [6]. Mỗi lượt ngoài huấn luyện trên 153 hoặc 154 chuyến, đánh giá trên 39 hoặc 38 chuyến tương ứng. Mọi mô hình chính dùng cùng 50 cách chia ngoài. Mỗi chuyến được giữ lại để đánh giá một lần trong mỗi lần lặp; dữ liệu telemetry của chuyến đó không vào huấn luyện vì đã gom theo chuyến trước khi chia. Cách chia ngẫu nhiên này vẫn cho phép cùng tuyến, ngày bay và cấu hình vận hành xuất hiện ở cả hai tập.

Với M2 và M3, GridSearchCV chọn siêu tham số bằng kiểm định chéo năm phần có xáo trộn bên trong tập huấn luyện ngoài, seed 301, tối ưu điểm âm của sai số tuyệt đối trung bình [6]. M1 dùng phép biến đổi bình phương tốc độ cố định rồi hồi quy tuyến tính, không cần lưới siêu tham số. MAE, RMSE và hệ số xác định R² được tính riêng trên từng tập đánh giá ngoài:

MAE = mean(|y − ŷ|);  RMSE = √mean((y − ŷ)²)     (2)

R² = 1 − ∑(y − ŷ)² / ∑(y − mean(y))²     (3)

Các bảng báo cáo trung bình và độ lệch chuẩn tổng thể của 50 điểm số, đúng cách tính trong code. Riêng biểu đồ chẩn đoán lấy trung bình mười dự đoán ngoài tập huấn luyện của mỗi chuyến. Không dùng chỉ số tính từ dự đoán đã lấy trung bình để thay kết quả theo fold. Tỷ lệ MAE trên năng lượng trung bình chỉ là chuẩn hóa, không phải sai số phần trăm tuyệt đối trung bình.

## III Kết quả

### A Phân tích khám phá dữ liệu

Năng lượng của các chuyến giữ lại có trung bình 21,27 Wh, độ lệch chuẩn 4,90 Wh, trung vị 20,79 Wh và khoảng 12,99–37,75 Wh. Tuyến R1 chiếm 180 trong 192 chuyến, tương đương 93,75%. Phần còn lại gồm một chuyến trên mỗi tuyến R2, R3, R4; bốn chuyến R5 và năm chuyến R6. Sự tập trung này có ý nghĩa: độ chính xác validation tổng thể chủ yếu phản ánh điều kiện được đại diện bởi R1.

![eda_VI.png](work/assets/eda_VI.png)

Hình 2. Năng lượng ghi nhận theo từng đầu vào chính. Mỗi chấm là một chuyến; đường đen nối trung bình nhóm. Dịch ngang nhỏ chỉ giúp tránh chồng chấm, không thay đổi mức cài đặt.

BẢNG III  Năng lượng trung bình và số chuyến theo mức vận hành

| Đầu vào | Các mức | Trung bình Wh | Số chuyến |
| --- | --- | --- | --- |
| Tốc độ m/s | 4 / 6 / 8 / 10 / 12 | 27,0 / 22,1 / 19,8 / 18,6 / 18,6 | 40 / 38 / 36 / 41 / 37 |
| Tải trọng g | 0 / 250 / 500 | 19,2 / 21,5 / 23,1 | 66 / 61 / 65 |
| Độ cao m | 25 / 50 / 75 / 100 | 17,4 / 20,5 / 22,6 / 25,2 | 53 / 47 / 47 / 45 |

Năng lượng trung bình giảm rõ từ 4 đến 8 m/s và gần như không đổi giữa 10 với 12 m/s. Ngược lại, tải trọng và độ cao có xu hướng tăng năng lượng. Đây là thống kê biên: trong mỗi nhóm vẫn còn khác biệt về các thông số khác và tuyến bay. Vì vậy, các hình mô tả mối liên hệ trong dữ liệu, chưa tách riêng tác động nhân quả của việc thay đổi một tham số.

EDA còn tính phân vị 90% của vận tốc ngang đo được trong từng chuyến. Trung bình chỉ số này theo tốc độ cài đặt đạt khoảng 9,65 m/s khi cài 10 m/s và 10,66 m/s khi cài 12 m/s. Kết quả phù hợp với lợi ích giảm dần ở mức cài cao nhất, nhưng chưa chứng minh tốc độ tối ưu vật lý phổ quát. Vận tốc đo được chỉ phục vụ chẩn đoán, không làm đầu vào. Thời gian bay tương quan mạnh với năng lượng, r = 0,83, nhưng bị loại vì giá trị thực tế chưa có trước cất cánh.

ANOVA và Kruskal–Wallis trong notebook EDA đều cho p < 0,001 khi so sánh các nhóm của từng đầu vào chính. Đây là bằng chứng thăm dò cho bước mô hình hóa; điều kiện vận hành dùng chung và nhiều phép so sánh hạn chế diễn giải nhân quả độc lập. Xu hướng cong theo tốc độ là cơ sở thử M1, còn xu hướng tăng theo tải và độ cao hỗ trợ giữ hai thành phần tuyến tính tương ứng.

### B Hiệu năng dự báo

BẢNG IV  Kết quả kiểm định chéo lặp lại trung bình ± độ lệch chuẩn

| Mô hình | MAE Wh | RMSE Wh | R² |
| --- | --- | --- | --- |
| B0 | 3,979 ± 0,432 | 4,903 ± 0,523 | -0,058 ± 0,112 |
| B1* | 4,007 ± 0,454 | 4,946 ± 0,532 | -0,077 ± 0,128 |
| B2 | 1,478 ± 0,168 | 1,937 ± 0,462 | 0,829 ± 0,072 |
| B3 | 1,478 ± 0,168 | 1,937 ± 0,462 | 0,829 ± 0,072 |
| B2 + cự ly* | 1,362 ± 0,106 | 1,675 ± 0,206 | 0,874 ± 0,030 |
| M1 | 0,849 ± 0,172 | 1,375 ± 0,549 | 0,908 ± 0,067 |
| M2 | 0,882 ± 0,212 | 1,537 ± 0,559 | 0,885 ± 0,077 |
| M3 | 0,833 ± 0,188 | 1,409 ± 0,548 | 0,903 ± 0,067 |

* Các biến thể cự ly mang tính thăm dò, dùng đại diện tuyến dựng trước kiểm định chéo. Kết quả không phải kiểm chứng độc lập cự ly kế hoạch trên tuyến mới.

M1 giảm MAE trung bình từ 1,4782 Wh của B2 xuống 0,8494 Wh, tương đương 42,5%. RMSE của M1 là 1,3755 Wh và R² trung bình là 0,9078. M3 có MAE thấp nhất, 0,8329 Wh; M1 có RMSE thấp nhất và R² trung bình cao nhất trong ba mô hình mới. MAE của M2 đạt 0,8818 Wh. Tỷ lệ MAE của M1 trên năng lượng trung bình bộ dữ liệu khoảng 4,0%; không có nghĩa mọi chuyến đều sai dưới 4%.

![oof_VI.png](work/assets/oof_VI.png)

Hình 3. Chẩn đoán M1 từ trung bình mười dự đoán ngoài tập huấn luyện của mỗi chuyến. Trái: thực tế so với dự đoán, kèm đường y = x. Phải: phần dư theo dự đoán; phần dư dương là dự đoán thiếu. R6 được tô riêng.

Ridge và hồi quy tuyến tính không điều chuẩn cho sai số gần như trùng nhau ở cấu hình này. Kết quả không chứng minh điều chuẩn luôn không cần thiết: alpha được cố định bằng 1 và các đầu vào chưa chuẩn hóa thang đo. Trong tìm kiếm lồng nhau, Random Forest chọn min_samples_leaf = 1 ở cả 50 lượt ngoài; Gradient Boosting chọn max_depth = 2 ở 45 lượt và bằng 3 ở năm lượt.

### C So sánh theo cặp và phân tích sai số

Code so sánh MAE theo cặp trên các fold ngoài bằng thống kê t có hiệu chỉnh theo Nadeau và Bengio [5]. Với K = 50 chênh lệch d và phương sai mẫu s², công thức là t = mean(d) / sqrt[(1/K + n_test/n_train)s²], với 49 bậc tự do. Tỷ lệ kích thước lấy từ lượt đầu, 39/153. Đây là hiệu chỉnh gần đúng cho sự phụ thuộc; các p-value chưa hiệu chỉnh cho nhiều so sánh theo cặp.

BẢNG V  So sánh MAE theo cặp có hiệu chỉnh

| Chênh lệch | Trung bình Wh | p-value |
| --- | --- | --- |
| B2 − M1 | 0,629 | 2.56e-12 |
| B2 − M2 | 0,596 | 1.97e-08 |
| B2 − M3 | 0,645 | 2.57e-11 |
| M1 − M3 | 0,017 | 7.89e-01 |
| M1 − M2 | -0,032 | 6.93e-01 |

Cả ba mô hình mới đều cải thiện so với B2 trên đủ 50 cách chia, với p có hiệu chỉnh < 0,001. M1 so với M3 cho p ≈ 0,79; M1 so với M2 cho p ≈ 0,69. Các so sánh chưa cung cấp bằng chứng về khác biệt MAE trung bình theo quy trình này. Kết quả không chứng minh tính tương đương và không nên được hiểu là các phương pháp có hiệu năng giống hệt nhau.

Với dự đoán ngoài tập huấn luyện đã lấy trung bình, B2 dự đoán thiếu hơn 2 Wh ở 26 chuyến; M1, M2 và M3 đều giảm số này xuống bảy. Năm trong bảy chuyến đó là toàn bộ năm chuyến R6. M1 có MAE 0,69 Wh trên R1–R5 nhưng 6,71 Wh trên R6. Chuyến 272, tiêu thụ cao nhất với 37,75 Wh, vẫn bị dự đoán thiếu lớn. Cải thiện sai số trung bình vì vậy chưa giải quyết được nhóm lỗi tập trung này.

### D Thử nghiệm giữ lại mức biên

Một thử nghiệm riêng loại toàn bộ chuyến ở một mức tốc độ hoặc độ cao biên khỏi huấn luyện, rồi đánh giá đúng mức bị loại. Siêu tham số mô hình cây được chọn trong dữ liệu huấn luyện còn lại. Thử nghiệm xét bốn mức cài đặt thiếu cụ thể; khác quy trình 50 điểm số theo fold và không phải phép thử tuyến mới.

BẢNG VI  MAE tính bằng Wh tại mức bị giữ lại

| Mức giữ lại | B2 | M1 | M2 | M3 |
| --- | --- | --- | --- | --- |
| Tốc độ 4 m/s | 4,34 | 1,66 | 5,02 | 4,99 |
| Tốc độ 12 m/s | 3,43 | 1,71 | 0,85 | 0,78 |
| Độ cao 25 m | 1,76 | 1,25 | 3,19 | 3,20 |
| Độ cao 100 m | 1,31 | 0,84 | 2,50 | 2,72 |

M1 có sai số thấp nhất ở ba trường hợp; M3 tốt nhất khi giữ lại mức 12 m/s. Vận tốc thực tế chỉ tăng hạn chế giữa mức cài 10 và 12 m/s là một giải thích phù hợp cho ngoại lệ này. Kết quả ủng hộ M1 như mô hình gọn nhẹ ở các mức biên đã thử, chưa xác lập khả năng ngoại suy an toàn ngoài phạm vi thí nghiệm.

## IV Thảo luận

### A Lựa chọn và diễn giải mô hình

Nghiên cứu chọn M1 vì cải thiện rõ so với baseline tuyến tính, đạt chỉ số tổng thể cạnh tranh, biểu diễn trực tiếp tác động của đầu vào và cho kết quả tốt ở ba thử nghiệm mức biên. Lựa chọn cân nhắc các bằng chứng, không chỉ dựa vào MAE nhỏ nhất. Công thức khớp trên toàn bộ dữ liệu là:

Ê = 32.1960 − 4.1944v + 0.1969v² + 0.0081m + 0.1050h     (4)

Năng lượng tính bằng Wh, tốc độ bằng m/s, tải bằng g và độ cao bằng m. Hệ số đã làm tròn để trình bày. Phương trình (4) được khớp trên đủ 192 chuyến để diễn giải; kết quả validation đến từ các mô hình khớp riêng trong từng fold. Đây không phải đánh giá độc lập bổ sung hoặc tệp mô hình sẵn sàng triển khai. Khi giữ các đầu vào khác cố định, hệ số tải tương ứng khoảng 0,81 Wh cho mỗi 100 g tăng thêm; hệ số độ cao tương ứng 2,63 Wh cho mỗi 25 m tăng thêm.

Thành phần bình phương tốc độ dương sửa khuôn mẫu cong trong phần dư B2. Parabol khớp có cực tiểu gần 10,7 m/s. Con số mô tả mô hình hiện tại trong phạm vi tốc độ cài đặt đã xét, không phải tốc độ vận hành tối ưu đã kiểm chứng. Cự ly, thời tiết, tình trạng pin, khả năng bám tốc độ và bất định dự báo chưa được mô hình hóa đầy đủ đều có thể thay đổi quyết định kế hoạch. Tương tự, dấu hệ số và xu hướng nhóm không xác lập quan hệ nhân quả.

### B Cự ly tuyến và thời điểm có thông tin

Phân tích GPS cho trung vị chiều dài đường ngang khoảng 472 m ở R1 và 837 m ở R6; trung vị các tuyến R2–R5 nằm khoảng 427–534 m. Đây là tổng chuyển động ngang ghi nhận, chưa được xác nhận là khoảng cách giao hàng một chiều. Không thể tự động nhân đôi thành nhiệm vụ khứ hồi hoặc coi là phạm vi giao hàng đã kiểm chứng. Khi thiếu cự ly, cùng v, m, h luôn cho cùng dự đoán dù tuyến dài khác nhau đáng kể. Hạn chế cấu trúc này giải thích vì sao chỉ tăng độ linh hoạt mô hình chưa sửa được lỗi R6.

Bổ sung đại diện cự ly tuyến vào B2 làm MAE kiểm định chéo lặp giảm từ 1,4782 xuống 1,3621 Wh. Chẩn đoán một lần chia năm phần trong notebook 03 còn giảm MAE R6 từ khoảng 6,85 xuống 2,8 Wh. Tuy nhiên, đại diện này được dựng từ tất cả chuyến của từng tuyến trước validation. Với tuyến chỉ có một chuyến, đó chính là chiều dài đường quan sát của chuyến ấy. Dù không dùng năng lượng mục tiêu để dựng cự ly, cách làm vẫn chưa phản ánh đánh giá đầu vào trước bay độc lập. Cần hình học tuyến kế hoạch hoặc đại diện được ước lượng chỉ trên dữ liệu huấn luyện để có kết luận mạnh hơn.

### C Giới hạn của bằng chứng hiện tại

Kiểm định chéo ngẫu nhiên theo chuyến đo hiệu năng trong bộ dữ liệu hiện có. Quy trình không giữ lại toàn bộ tuyến, ngày hoặc cấu hình vận hành và chưa thử dữ liệu bên ngoài. Quy tắc chọn mẫu cùng quyết định thêm bình phương tốc độ được hình thành sau khi khám phá chính bộ dữ liệu này. Tìm siêu tham số lồng nhau kiểm soát lựa chọn tham số cây, nhưng không loại bỏ mọi thiên lệch lạc quan khi chọn họ mô hình sau khi xem kết quả. R6 chỉ có năm chuyến nên ước lượng riêng tuyến còn bất định.

MAE thấp hoặc sai số mức biên thuận lợi chưa xác lập an toàn bay. Chưa có hàm quyết định kết hợp dung lượng pin khả dụng, hành trình đi và về, dự phòng 20% hoặc ngưỡng sạc 25%. Khoảng dự đoán giải tích trong notebook baseline dựa trên giả định tuyến tính và kiểm tra độ phủ gần đúng; chưa phải khoảng đã hiệu chuẩn cho M1. Mô hình bất định được kiểm chứng độc lập và giả định pin rõ ràng là điều kiện cho lớp quyết định Fly hoặc No-fly sau này.

## V Kết luận

Trên 192 chuyến giữ lại, hồi quy với tốc độ cài đặt, bình phương tốc độ, tải trọng và độ cao cài đặt đạt MAE 0,849 Wh, RMSE 1,375 Wh và R² trung bình 0,908 bằng kiểm định chéo năm phần lặp mười lần. Bổ sung bình phương tốc độ giảm MAE 42,5% so với baseline tuyến tính. Sai số cạnh tranh với các tổ hợp cây được chọn siêu tham số, đồng thời tốt nhất ở ba trong bốn thử nghiệm mức biên. Kết quả ủng hộ mô hình gọn nhẹ, dễ diễn giải cho dự báo năng lượng trong điều kiện được dữ liệu đại diện.

Dự đoán thiếu có hệ thống trên đủ năm chuyến R6 là hạn chế chính chưa giải quyết. Hướng tiếp theo gồm cung cấp cự ly kế hoạch biết trước độc lập, đánh giá bằng cách giữ lại tuyến và ngày, định lượng bất định dự báo, kiểm tra độ nhạy theo ranh giới bản ghi và quy tắc loại trừ. Tình trạng pin, dự báo thời tiết và yêu cầu lượt về cần dữ liệu cùng kiểm chứng cụ thể trước khi dùng dự báo năng lượng để hỗ trợ quyết định bay thực tế.

### Khả năng tái lập

Phân tích nằm trong bốn notebook theo thứ tự làm sạch, EDA, baseline và thực nghiệm. Các phép ngẫu nhiên dùng seed 301. Toàn bộ thực nghiệm chính, baseline và thử nghiệm mức biên đã được chạy lại cho bản thảo, khớp các bảng lưu ở độ chính xác công bố. Nhãn năng lượng được tính lại độc lập từ điện áp, dòng điện và thời gian thô. Môi trường kiểm chứng dùng Python 3.11.9, NumPy 2.4.6, pandas 3.0.3, SciPy 1.17.1 và scikit-learn 1.9.1. Biểu đồ chẩn đoán dùng cùng dữ liệu và cách chia, không bổ sung đầu vào dự báo.

### Tài liệu tham khảo

[1] T. A. Rodrigues et al., “In-flight positional and energy use data set of a DJI Matrice 100 quadcopter for small package delivery,” Scientific Data, vol. 8, art. 155, 2021, doi: 10.1038/s41597-021-00930-x. https://arxiv.org/abs/2103.13313

[2] T. A. Rodrigues et al., “Data Collected with Package Delivery Quadcopter Drone,” KiltHub, dataset, doi: 10.1184/R1/12683453. https://doi.org/10.1184/R1/12683453

[3] T. A. Rodrigues, J. Patrikar, N. L. Oliveira, H. S. Matthews, S. Scherer, and C. Samaras, “Drone flight data reveal energy and greenhouse gas emissions savings for very small package delivery,” Patterns, vol. 3, no. 8, art. 100569, 2022, doi: 10.1016/j.patter.2022.100569.

[4] F. Pedregosa et al., “Scikit-learn: Machine Learning in Python,” Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011. https://jmlr.org/papers/v12/pedregosa11a.html

[5] C. Nadeau and Y. Bengio, “Inference for the Generalization Error,” Machine Learning, vol. 52, pp. 239–281, 2003, doi: 10.1023/A:1024068626366.

[6] Scikit-learn developers, “RepeatedKFold” and “GridSearchCV,” API documentation, accessed Nov. 3, 2026. https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RepeatedKFold.html ; https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
