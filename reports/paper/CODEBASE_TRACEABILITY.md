# Đối chiếu paper với codebase

Hai bản EN và VI dùng cùng thí nghiệm, bảng và hình; khác ngôn ngữ trình bày. Bản thảo bám working tree hiện tại, bao gồm thay đổi chưa commit, tại commit nền `eee0abc2acba559c4179d9076e25aa05b69c66b7`. Không sửa bốn notebook hoặc bảng kết quả gốc khi viết paper.

## Nguồn của từng nội dung

Chỉ số cell dưới đây đánh số từ 0 trong JSON notebook.

| Nội dung paper | Nguồn trong repository | Kiểm chứng |
|---|---|---|
| 209 chuyến thô, 257.896 dòng telemetry; loại 17, còn 192 | `notebooks/01_data_cleaning.ipynb`, `reports/exclusion_log.csv`, `data/processed/flight_level.csv` | Đọc nguồn và đối chiếu dữ liệu |
| Nhãn Wh theo tích phân hình thang | Notebook 01, cell 71, 73, 76 | Tính lại độc lập từ dữ liệu thô, sai khác dưới 1e-10 Wh |
| Khoảng ghi và đối chiếu Riemann | Notebook 01, cell 9, 82 | Dùng thống kê dữ liệu/output hiện có |
| EDA theo tải, tốc độ, độ cao và phân vị vận tốc | `notebooks/02_eda.ipynb`, cell 17, 18, 20, 26, 33 | Hình EDA tái dựng từ cùng bảng flight_level và seed 301 |
| Baseline B0/B1/B2/B3, B2 cộng cự ly | `notebooks/03_baseline_model.ipynb`, cell 6, 9, 11, 22, 29 | Chạy lại code, trung bình metric khớp `reports/baseline_results.csv` ở độ chính xác đã lưu |
| M1/M2/M3, nested CV, metric 50 lượt | `notebooks/04_experiment_evaluation.ipynb`, cell 2, 3, 5, 7, 9 | Chạy lại trực tiếp các cell nguồn, trung bình metric khớp `reports/experiment_results.csv` ở độ chính xác đã lưu |
| Kiểm định t có hiệu chỉnh | Notebook 04, cell 14 | Tính lại cùng công thức với tỷ lệ 39/153 và 49 bậc tự do |
| Phần dư và các chuyến R6 | Notebook 04, cell 17, 20–22 | Tính lại từ dự đoán OOF trung bình mười lần/chuyến |
| Thử bỏ mức tốc độ/độ cao biên | Notebook 04, cell 25 | Chạy lại cell nguồn, toàn bộ 16 giá trị MAE khớp bảng hai chữ số thập phân |
| Công thức M1 khớp toàn bộ dữ liệu | Notebook 04, cell 28 | Tính lại hệ số bằng `numpy.linalg.lstsq` |

## Hình được tạo cho paper

- Hình 1: công suất chuyến 1, cùng điện áp, dòng điện và thời gian như notebook 01.
- Hình 2: tái trình bày EDA theo cùng dữ liệu và logic notebook 02. Hai ngôn ngữ có nhãn trục tương ứng.
- Hình 3: bổ sung đồ thị actual–predicted và residual của M1, dùng đúng trung bình mười dự đoán OOF/chuyến từ notebook 04. Không phải kết quả huấn luyện trên toàn bộ dữ liệu. Không dùng các dự đoán đã trung bình để thay metric validation theo fold.

## Những giới hạn được giữ rõ trong paper

- Cự ly chỉ là biến bổ sung thăm dò; không thuộc ba đầu vào của so sánh chính. Trung vị GPS theo route được tính trước chia tập, chưa phải đánh giá cự ly kế hoạch độc lập.
- Tổng đường GPS ngang chưa được xác nhận là khoảng cách giao hàng một chiều; không tự động nhân đôi cho khứ hồi.
- Random CV theo chuyến không kiểm chứng tuyến/ngày/cấu hình hoàn toàn mới.
- Chưa phát hiện khác biệt thống kê giữa M1 và mô hình cây không đồng nghĩa chứng minh tương đương.
- Bài không tuyên bố an toàn bay, tốc độ tối ưu vận hành, hiệu năng ngoài phạm vi dữ liệu hoặc đã có luật Fly/No-fly.
- Chưa có SoC, SoH hoặc dự báo thời tiết làm đầu vào.
- Bảng lưới siêu tham số và việc không chuẩn hóa Ridge phản ánh đúng code hiện tại.

## Các tệp hỗ trợ tái lập

- `work/verify_results.py`: chạy lại thí nghiệm chính và kiểm tra nhãn năng lượng; dùng môi trường Python nghiên cứu của máy.
- `work/verify_secondary.py`: kiểm tra baseline, GPS, thí nghiệm mức biên.
- `work/verification.json`: metric chưa làm tròn, phiên bản thư viện, SHA-256 của notebook và dữ liệu đã dùng.
- `work/secondary_verification.json`: kết quả kiểm chứng baseline, cự ly và mức biên.
- `work/oof_predictions.csv`: dự đoán dùng cho chẩn đoán.
- `work/build_papers.py`: tạo Word và hình; dùng Python đóng gói và thư viện tạo tài liệu.

## Lưu ý trước khi nộp

Tên tác giả đang để nhóm đồ án DTA301 và trường FPT do README chưa có danh sách thành viên. Cần bổ sung đúng tên, mã sinh viên, email và thông tin lớp nếu giảng viên yêu cầu. Hai bản dùng cấu trúc nội dung IEEE, trình bày một cột A4; chưa áp dụng template riêng của một tạp chí hoặc hội nghị. Mỗi bản có 8 trang theo bản render đã kiểm tra.

Trình render LibreOffice đóng gói không khả dụng trên Windows này (`soffice.exe` không được tìm thấy). Kiểm tra bố cục được thực hiện bằng Word xuất PDF, sau đó Poppler đóng gói xuất ảnh từng trang; các ảnh được kiểm tra trực quan. PDF và ảnh trong `work` là tệp QA.
