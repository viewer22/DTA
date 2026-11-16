"""Vẽ sơ đồ quy trình (Hình phương pháp) dùng chung cho paper và slide."""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
plt.rcParams.update({"font.family": "DejaVu Sans", "savefig.dpi": 300})
NAVY, ORANGE, GRAY = "#1B3550", "#E07B24", "#9AA5B1"

fig, ax = plt.subplots(figsize=(7.16, 2.55))
ax.set_xlim(0, 99.5); ax.set_ylim(0, 36); ax.axis("off")

def hop(x, y, w, h, tieu_de, noi_dung, mau, nen="white", ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=nen, ec=mau, lw=1.4, ls=ls))
    ax.text(x + w / 2, y + h - 2.2, tieu_de, ha="center", va="top", fontsize=7.0, fontweight="bold", color=mau)
    ax.text(x + w / 2, y + h - 6.6, noi_dung, ha="center", va="top", fontsize=6.4, color="#222", linespacing=1.35)

def mui_ten(x1, y1, x2, y2, mau="#444", ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=9, lw=1.1, color=mau, ls=ls))

ax.text(0.5, 35, "Phần chính: dự đoán năng lượng (Energy Prediction)", fontsize=7.8, fontweight="bold", color=NAVY, va="top")
y0, h = 13.5, 18
cot = [("1. Đầu vào", "Tốc độ cài đặt v\nTải m\nĐộ cao cài đặt h\n(biết trước khi bay)"),
       ("2. Tạo đặc trưng", "Thêm v²\n(EDA: E giảm rồi\nchững theo v)\nLoại biến rò rỉ"),
       ("3. Huấn luyện M1", "Hồi quy OLS\nÊ = β₀+β₁v+β₂v²\n+β₃m+β₄h"),
       ("4. Đánh giá", "5-fold × 10 lần,\nseed 301; MAE,\nRMSE, R², t-test\nNadeau–Bengio"),
       ("5. Dự đoán", "Ê (Wh) cho\nchuyến sắp bay")]
w, gap = 16.6, 3.6
for i, (t, n) in enumerate(cot):
    x = 0.8 + i * (w + gap)
    hop(x, y0, w, h, t, n, ORANGE if i in (2, 4) else NAVY, nen="#FDF3EA" if i in (2, 4) else "white")
    if i < len(cot) - 1:
        mui_ten(x + w + 0.6, y0 + h / 2, x + w + gap - 0.6, y0 + h / 2)

ax.text(0.5, 10.5, "So sánh: B0–B3 (baseline);\nM2 Random Forest, M3 Gradient\nBoosting (đối chứng); cùng 3 biến,\ncùng 50 cách chia.",
        fontsize=6.4, color="#444", va="top")
# Lớp quyết định: tách riêng, nét đứt
xd = 0.8 + 4 * (w + gap)
ax.add_patch(FancyBboxPatch((36, 0.4), xd + w - 36, 6.0, boxstyle="round,pad=0.3,rounding_size=1", fc="#F2F4F7", ec=GRAY, lw=1.1, ls="--"))
ax.text(37, 3.4, "Ứng dụng minh họa, tách riêng (Decision Layer): cận trên Ê·q90 so với\npin dùng được → FLY / CONDITIONAL / NO-FLY; 4.800 kịch bản bán mô phỏng", fontsize=6.0, color="#333", va="center")
mui_ten(xd + w / 2, y0 - 0.6, xd + w / 2, 7.0, mau=GRAY, ls="--")
plt.savefig(ROOT / "reports" / "figures" / "final_pipeline.png", bbox_inches="tight", pad_inches=0.03)
print("ok")
