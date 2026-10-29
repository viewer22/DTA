# DTA301: Safety-Aware Pre-Flight Energy Feasibility for Delivery UAV

Dự đoán năng lượng tiêu thụ của một chuyến giao hàng bằng drone từ các thông số biết trước khi bay, dùng dữ liệu bay thật của CMU (DJI Matrice 100).

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

Chạy các notebook trong `notebooks/` theo đúng thứ tự số. Seed cố định: 301.

## Cấu trúc

```
data/raw/          dữ liệu gốc (tự tải)
data/processed/    dữ liệu đã xử lý, sinh ra từ notebook 01
notebooks/
  01_data_cleaning.ipynb
  02_eda.ipynb
  03_baseline_model.ipynb
  04_experiment_evaluation.ipynb
src/               hàm dùng lại giữa các notebook
reports/           bảng kết quả, nhật ký loại trừ
reports/figures/   hình
slides/            slide thuyết trình
```

## Tiến độ

| Tuần | Báo cáo môn | Notebook | Xong |
|---|---|---|---|
| W3 | D1 Proposal | | [ ] |
| W4 | D2 EDA | 01, 02 | [ ] |
| W5 | D3 Baseline | 03 | [ ] |
| W8 | D4 Experiment | 04 | [ ] |
| W10 | D5 Final | tất cả | [ ] |

## Khai báo

- Reproducibility Statement: (viết ở D5)
- AI Usage Declaration: (viết ở D5)
