# DTA301: Safety-Aware Pre-Flight Energy Feasibility for Delivery UAV

Dự đoán năng lượng tiêu thụ của một chuyến giao hàng bằng drone từ các thông số biết trước khi bay, dùng dữ liệu bay thật của CMU (DJI Matrice 100), rồi dùng dự đoán đó để ra phán quyết FLY / CONDITIONAL / NO-FLY.

## Kết quả chính

| Câu hỏi | Kết quả |
|---|---|
| RQ chính: dự đoán năng lượng từ tốc độ, tải, độ cao | M1 (hồi quy + speed²): MAE 0,85 Wh (≈ 4%), R² 0,91 trên 5-fold × 10, seed 301 |
| Phụ 1: ít bay sai hơn ngưỡng % pin? | Bay sai 0,6% (theo M1) so với 5,9% (SoC ≥ 50%), trên 4.800 kịch bản |
| Phụ 2: 3 mức giảm huỷ nhầm? | Huỷ nhầm 13,6% → 3,0%, bay sai giữ 0,6% |

Paper: `reports/DTA301_Final_Paper.docx` · Slide: `slides/DTA301_Final_Slides.pptx`

Bản cũ của nhóm nằm trong lịch sử git (commit `477f799`).

## Nhóm

| Vai trò | Thành viên |
|---|---|
| Leader | |
| Data Engineer | |
| Analyst | |
| Modeler | |
| Reporter | |

## Dữ liệu

Tải 2 file từ KiltHub (CMU, DOI [10.1184/R1/12683453](https://doi.org/10.1184/R1/12683453), giấy phép CC BY 4.0) và đặt vào `data/raw/`:

- `parameters.csv`
- `flights.csv` (~102 MB, không commit)

## Cách chạy

```bash
pip install -r requirements.txt
jupyter notebook
```

Chạy các notebook trong `notebooks/` theo đúng thứ tự số (01 → 06). Seed cố định: 301. Notebook 04–05 chỉ cần `data/processed/flight_level.csv` (đã có trong repo), nên chạy được ngay mà không cần tải dữ liệu thô; notebook 03 và 06 cần thêm `data/raw/flights.csv` để tính cự ly tuyến.

## Cấu trúc

```
data/raw/          dữ liệu gốc (tự tải)
data/processed/    dữ liệu đã xử lý, sinh ra từ notebook 01
notebooks/
  01_data_cleaning.ipynb
  02_eda.ipynb
  03_baseline_model.ipynb
  04_experiment_evaluation.ipynb
  05_decision_layer.ipynb       lớp quyết định FLY / CONDITIONAL / NO-FLY
  06_m1_evaluation_final_figures.ipynb   đánh giá M1 (hệ số, actual vs predicted, phần dư, R6), bộ hình final_*.png cho paper và slide
src/               hàm dùng lại giữa các notebook
reports/           bảng kết quả, nhật ký loại trừ
reports/figures/   hình
slides/            slide thuyết trình
```

## Tiến độ

| Tuần | Báo cáo môn | Notebook | Xong |
|---|---|---|---|
| W3 | D1 Proposal | | [x] |
| W4 | D2 EDA | 01, 02 | [x] |
| W5 | D3 Baseline | 03 | [x] |
| W8 | D4 Experiment | 04 | [x] |
| W10 | D5 Final | tất cả + 05 | [x] |

## Khai báo

**Reproducibility Statement.** Tải `parameters.csv` và `flights.csv` từ KiltHub (DOI 10.1184/R1/12683453, CC BY 4.0) vào `data/raw/`, `pip install -r requirements.txt`, rồi chạy notebook 01 → 06 (`python src/make_pipeline_fig.py` vẽ sơ đồ quy trình). Seed 301 cho mọi cách chia và kịch bản. Bảng kết quả: `reports/baseline_results.csv`, `experiment_results.csv`, `decision_results.csv`, `decision_robustness.csv`, `exclusion_log.csv`, `final_model_table.csv`, `final_numbers.json`; hình: `reports/figures/` (paper và slide dùng chung `final_*.png`). Báo cáo D1–D5: `reports/deliverables/`.

**Giả định ở notebook 05.** Trạng thái pin (SoC, SoH, nhiệt độ) là mô phỏng; năng lượng chuyến bay là đo thật. Pin 99,9 Wh (TB47D), SoC ~ U(0,15; 1), SoH ~ U(0,7; 1), T ~ U(−10; 40) °C, dự trữ hạ cánh 20% SoC. Kết quả là so sánh tương đối giữa các luật, không phải chứng nhận an toàn bay.

**AI Usage Declaration.** Nhóm dùng Claude (Anthropic) để hỗ trợ giải thích khái niệm, gợi ý code phân tích (bao gồm notebook 05), soạn thảo và biên tập báo cáo, slide. Nhóm tự chạy lại notebook, kiểm tra code, đối chiếu từng con số với file kết quả và chịu trách nhiệm toàn bộ nội dung.
