# -*- coding: utf-8 -*-
"""
BƯỚC 1 - CHỈ NHÌN DỮ LIỆU, CHƯA PHÂN TÍCH GÌ.

Cách chạy trong IntelliJ: chuột phải vào file này -> Run 'buoc1_xem_du_lieu'.
Đọc từng khối một, chạy xong so kết quả với chú thích.
"""
from pathlib import Path

import pandas as pd

# Thư mục data/raw nằm ở gốc repo, tức là cha của thư mục chứa file này.
RAW = Path(__file__).resolve().parent.parent / "data" / "raw"

# ---------------------------------------------------------------------------
# KHỐI 1: parameters.csv = KẾ HOẠCH của từng chuyến bay (1 dòng = 1 chuyến)
# ---------------------------------------------------------------------------
params = pd.read_csv(RAW / "parameters.csv")

print("=== parameters.csv ===")
print("So dong, so cot:", params.shape)        # (209, 7) -> 209 chuyến, 7 cột
print(params.head())                            # 5 dòng đầu

# value_counts() = đếm mỗi giá trị xuất hiện bao nhiêu lần
for col in ["speed", "payload", "altitude", "route"]:
    print(f"\n--- {col} ---")
    print(params[col].value_counts().sort_index())

# ---------------------------------------------------------------------------
# KHỐI 2: flights.csv = NHẬT KÝ ĐO trong lúc bay (1 dòng = 1 khoảnh khắc)
# ---------------------------------------------------------------------------
# low_memory=False để pandas đọc cả file rồi mới đoán kiểu, tránh cảnh báo
flights = pd.read_csv(RAW / "flights.csv", low_memory=False)

print("\n=== flights.csv ===")
print("So dong, so cot:", flights.shape)       # (257896, 28)
print("Ten cot:", list(flights.columns))
print("So chuyen bay khac nhau:", flights["flight"].nunique())   # 209, khớp file 1

# ---------------------------------------------------------------------------
# KHỐI 3: phóng to vào MỘT chuyến bay (chuyến số 1)
# ---------------------------------------------------------------------------
f1 = flights[flights["flight"] == 1]           # lọc: chỉ giữ dòng của chuyến 1

print("\n=== Chuyen 1 ===")
print("So dong do:", len(f1))
print(f1[["time", "battery_voltage", "battery_current"]].head(10))

# diff() = hiệu của dòng này trừ dòng trước -> khoảng cách thời gian giữa 2 mẫu
buoc = f1["time"].diff().dropna()
print("\nKhoang cach giua 2 mau (giay):")
print(buoc.describe())                          # trung bình ~0.15 s, KHÔNG đều nhau
