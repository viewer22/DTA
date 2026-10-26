# -*- coding: utf-8 -*-
"""
BƯỚC 2 - LỌC CHUYẾN BAY BẰNG CODE.

Hai phần:
  PHẦN A: dùng code để TÌM RA luật lọc (không đoán, không nhờ ai scan).
  PHẦN B: áp luật, ghi lý do từng chuyến bị loại, kiểm còn đúng 192 chuyến.

Chạy: chuột phải file -> Run. Đặt file trong DTA/notebooks/.
"""
from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
params = pd.read_csv(RAW / "parameters.csv")
print("Tong so chuyen trong parameters.csv:", len(params))   # 209

# ===========================================================================
# PHẦN A: TÌM RA LUẬT BẰNG CODE
# ===========================================================================
# Bài báo nói nhóm CMU bay theo lưới: payload 0/250/500 g, độ cao 25/50/75/100 m,
# tốc độ 4-12 m/s. Ta đếm giá trị thật trong data để xem cái gì nằm NGOÀI lưới.

print("\n--- A1. route ---")
print(params["route"].value_counts())
# -> thấy A1, A2, A3, H: không phải tuyến giao hàng

print("\n--- A2. Cac chuyen route A* / H co speed, altitude bao nhieu? ---")
print(params[params["route"].str.startswith(("A", "H"))][["flight", "route", "speed", "altitude"]])
# -> speed = 0, altitude = 0 hoặc 3: đứng yên dưới đất hoặc bay treo

print("\n--- A3. altitude ---")
print(params["altitude"].value_counts())
# -> thấy "0", "3", "25-50-100-25": ngoài lưới 25/50/75/100

print("\n--- A4. payload ---")
print(params["payload"].value_counts())
# -> thấy 750: ngoài lưới 0/250/500

print("\n--- A5. Dong dien trung vi cua tung chuyen (5 chuyen thap nhat) ---")
flights = pd.read_csv(RAW / "flights.csv", low_memory=False,
                      usecols=["flight", "battery_current"])
# groupby("flight") = gom các dòng theo chuyến, rồi lấy trung vị dòng điện mỗi chuyến
median_current = flights.groupby("flight")["battery_current"].median().sort_values()
print(median_current.head(5))
# -> drone đang bay rút hàng chục A. Chuyến nào trung vị gần 0 A mà KHÔNG phải
#    A*/H thì là cảm biến hỏng. Nhóm đặt ngưỡng 1.0 A.

# ===========================================================================
# PHẦN B: ÁP LUẬT VÀ GHI LÝ DO
# ===========================================================================
VALID_ALT = ["25", "50", "75", "100"]
VALID_PAYLOAD = [0, 250, 500]
CURRENT_THRESHOLD_A = 1.0

log = []          # nhật ký: mỗi chuyến bị loại 1 dòng, có lý do
df = params.copy()

# Luật 1: route bắt đầu bằng A hoặc H
mask = df["route"].str.startswith(("A", "H"))
for f in df.loc[mask, "flight"]:
    log.append({"flight": f, "reason": "khong bay hanh trinh (route A*/H)"})
df = df[~mask]    # dấu ~ nghĩa là "KHÔNG": giữ những dòng không bị đánh dấu

# Luật 2: độ cao ngoài lưới
mask = ~df["altitude"].astype(str).isin(VALID_ALT)
for f, a in df.loc[mask, ["flight", "altitude"]].values:
    log.append({"flight": f, "reason": f"do cao ngoai luoi ({a})"})
df = df[~mask]

# Luật 3: payload ngoài lưới
mask = ~df["payload"].isin(VALID_PAYLOAD)
for f, p in df.loc[mask, ["flight", "payload"]].values:
    log.append({"flight": f, "reason": f"payload ngoai luoi ({p})"})
df = df[~mask]

# Luật 4: cảm biến dòng hỏng (cần flights.csv, đã tính median_current ở A5)
bad = [f for f in df["flight"] if median_current.get(f, 0) < CURRENT_THRESHOLD_A]
for f in bad:
    log.append({"flight": f, "reason": f"cam bien dong hong ({median_current[f]:.2f} A)"})
df = df[~df["flight"].isin(bad)]

# ===========================================================================
# KẾT QUẢ
# ===========================================================================
log = pd.DataFrame(log)
log["flight"] = log["flight"].astype(int)
print("\n=== KET QUA ===")
print("Giu lai:", len(df), "chuyen")         # kỳ vọng 192
print("Bi loai:", len(log), "chuyen")        # kỳ vọng 17
print(log["reason"].str.split(" \\(").str[0].value_counts())
print("\nNhat ky loai tru:")
print(log.to_string(index=False))

# Kiểm tra: giữ + loại phải bằng tổng, không chuyến nào biến mất lặng lẽ
assert len(df) + len(log) == len(params)
