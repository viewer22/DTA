# DTA301: Safety-Aware Pre-Flight Energy Feasibility for Delivery UAV

Làm lại từ đầu. Bản cũ nằm trong lịch sử git (commit `477f799`).

## Dữ liệu

Tải 2 file từ KiltHub (CMU, DOI [10.1184/R1/12683453](https://doi.org/10.1184/R1/12683453), giấy phép CC BY 4.0):

- `parameters.csv`
- `flights.csv`

Đặt vào `data/raw/`. Thư mục này không được commit (xem `.gitignore`).

## Cấu trúc

```
data/raw/      dữ liệu gốc (tự tải)
notebooks/     từng bước, chạy theo thứ tự số
src/           hàm dùng lại nhiều lần (viết sau)
reports/       bảng, hình, nhật ký loại trừ
```

## Tiến độ

- [ ] Bước 1: xem dữ liệu
- [ ] Bước 2: lọc chuyến bay
- [ ] Bước 3: tính năng lượng từng chuyến
- [ ] Bước 4: bảng 1 dòng = 1 chuyến
