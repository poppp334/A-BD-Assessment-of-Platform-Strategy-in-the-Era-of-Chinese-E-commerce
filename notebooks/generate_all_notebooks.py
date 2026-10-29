"""Build and execute all 6 Jupyter notebooks for shopee-bd-analysis."""

import os
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from nbclient import NotebookClient

BASE_DIR = "/home/windows/Projects/Lab/shopee-bd-analysis"
NB_DIR = os.path.join(BASE_DIR, "notebooks")

def build_and_run_notebook(filename, cells):
    nb = new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.13",
            },
        },
    )
    nb_path = os.path.join(NB_DIR, filename)
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    client = NotebookClient(
        nb,
        timeout=120,
        kernel_name="python3",
        resources={"metadata": {"path": NB_DIR}},
    )
    client.execute()
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"Executed and saved: {filename}")


# ==============================================================================
# NOTEBOOK 01: Market Shift
# ==============================================================================
nb01_cells = [
    new_markdown_cell(
        """# Section 1 — Market Shift: ตลาดเปลี่ยนไปแล้ว
**Business Question:** Shopee ยังเป็นผู้นำแบบเดิมอยู่หรือไม่?

### ข้อมูลที่ใช้ (Verified Public Data)
- **Cube Asia (Tradewinds Dataset 2024–H1 2026) & Momentum Works:**
  - ภาพรวมปี 2025 ตลาดอีคอมเมิร์ซไทย (3 เจ้าหลัก) มีมูลค่า GMV รวม **$30.7B** (Shopee 51.8%, TikTok Shop 36.5%, Lazada 11.7%)
  - ในครึ่งแรกของปี 2026 (H1 2026) ตลาดเข้าสู่จุดสมดุล (46% : 46%) และในไตรมาส **Q2 2026** TikTok Shop แซงขึ้นเป็นอันดับ 1 รายไตรมาสครั้งแรกที่ **48%** ต่อ **45%** (Lazada เหลือ 7%)"""
    ),
    new_code_cell(
        """import os
import pandas as pd
import matplotlib.pyplot as plt
import chart_style

chart_style.setup_plot_style()
COLORS = chart_style.COLORS

q_df = pd.read_csv("../data/processed/sec01_gmv_quarterly.csv")
g_df = pd.read_csv("../data/processed/sec01_yoy_growth.csv")
display(q_df)
display(g_df)"""
    ),
    new_markdown_cell(
        """### กราฟ 1.1 — GMV Share Trajectory (Q1 2025 -> Q2 2026)
- **สื่ออะไร:** ส่วนต่างส่วนแบ่งตลาดหดตัวอย่างรวดเร็วและเกิดจุดตัด (Crossover) ใน Q2 2026 ตลาดอีคอมเมิร์ซไทยเปลี่ยนผ่านจากยุคผูกขาดรายเดียวเข้าสู่โครงสร้าง **Two-Pole (สองขั้วอำนาจ)**"""
    ),
    new_code_cell(
        """fig, ax = plt.subplots(figsize=(10.5, 6.0))

x = range(len(q_df))
quarters = q_df["quarter"].tolist()

# Shaded area from crossover zone (Q1 2026 -> Q2 2026)
ax.axvspan(3.65, 5.15, color="#FFE4E6", alpha=0.55, zorder=1, label="Two-Pole / Crossover Zone")

# Plot 3 platform lines (Shopee thicker per design rule)
ax.plot(x, q_df["shopee_share"], marker="o", markersize=8, linewidth=3.8,
        color=COLORS["Shopee"], label="Shopee (ผู้นำเดิม)", zorder=4)
ax.plot(x, q_df["tiktok_share"], marker="s", markersize=7.5, linewidth=2.8,
        color=COLORS["TikTok Shop"], label="TikTok Shop (ผู้ท้าชิง)", zorder=5)
ax.plot(x, q_df["lazada_share"], marker="^", markersize=7, linewidth=2.2,
        color=COLORS["Lazada"], linestyle="--", label="Lazada", zorder=3)

# Direct data labels on points
for i, row in q_df.iterrows():
    shopee_offset = 1.8 if i < 5 else -3.0
    tiktok_offset = -3.0 if i < 5 else 2.0
    ax.text(i, row["shopee_share"] + shopee_offset, f'{row["shopee_share"]:.1f}%',
            ha="center", va="center", fontsize=9.5, fontweight="bold", color=COLORS["Shopee"])
    ax.text(i, row["tiktok_share"] + tiktok_offset, f'{row["tiktok_share"]:.1f}%',
            ha="center", va="center", fontsize=9.5, fontweight="bold", color=COLORS["TikTok Shop"])
    ax.text(i, row["lazada_share"] - 2.4, f'{row["lazada_share"]:.1f}%',
            ha="center", va="center", fontsize=9, color=COLORS["Lazada"])

# Highlight Q2 2026 overtake point
ax.scatter([5], [48.0], s=190, facecolors="none", edgecolors=COLORS["TikTok Red"], linewidths=2.5, zorder=6)
ax.annotate(
    "จุดตัดประวัติศาสตร์ (Q2 2026)\\nTikTok Shop แซง Shopee (48% vs 45%)",
    xy=(5, 48.0), xytext=(2.6, 56.0),
    fontsize=10, fontweight="bold", color="#991B1B",
    bbox=dict(boxstyle="round,pad=0.45", facecolor="#FEF2F2", edgecolor=COLORS["TikTok Red"], lw=1.2),
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2", color=COLORS["TikTok Red"], lw=1.8),
    zorder=7
)

ax.set_xticks(list(x))
ax.set_xticklabels(quarters, fontweight="bold")
ax.set_ylabel("ส่วนแบ่ง GMV (%)", fontweight="bold")
ax.set_ylim(0, 64)
ax.set_xlim(-0.3, 5.35)
ax.legend(loc="center left", bbox_to_anchor=(0.01, 0.36), ncol=2)

chart_style.add_title_and_source(
    ax,
    title="TikTok Shop แซง Shopee ครั้งแรกใน Q2 2026 (48% vs 45%) — ตลาดเข้าสู่ยุค Two-Pole",
    subtitle="ส่วนแบ่งมูลค่าซื้อขายสินค้า (Physical-Goods GMV Share %) รายไตรมาสในประเทศไทย (Q1 2025 - Q2 2026)",
    source_text="Cube Asia (Tradewinds Dataset 2025-H1 2026) & Momentum Works"
)

plt.savefig("../charts/01_1_gmv_share_trajectory.png")
plt.show()"""
    ),
    new_markdown_cell(
        """### กราฟ 1.2 — Growth Rate Comparison (YoY %)
- **สื่ออะไร:** การแซงของ TikTok Shop ไม่ใช่เหตุการณ์ชั่วคราว แต่เกิดจากอัตราการเติบโต YoY ที่สูงกว่า Shopee กว่า 2.3 เท่า (+53.4% vs +23.3% ในปี 2025 และเร่งตัวต่อเนื่องใน H1 2026) ขณะที่ Lazada สูญเสียส่วนแบ่งอย่างหนัก"""
    ),
    new_code_cell(
        """import numpy as np

fig, ax = plt.subplots(figsize=(10.0, 5.8))

platforms = g_df["platform"].tolist()
x = np.arange(len(platforms))
width = 0.35

yoy_2025 = g_df["yoy_growth_pct"].tolist()
h1_2026 = g_df["h1_2026_annualized_growth_pct"].tolist()

bar_colors_2025 = [COLORS["Shopee"], COLORS["TikTok Shop"], COLORS["Lazada"]]
bar_colors_2026 = ["#FF8A65", COLORS["TikTok Red"], "#5C6BC0"]

rects1 = ax.bar(x - width/2, yoy_2025, width, label="อัตราเติบโตปี 2025 YoY (%)", color=bar_colors_2025, edgecolor="none", zorder=3)
rects2 = ax.bar(x + width/2, h1_2026, width, label="โมเมนตัมครึ่งแรก H1 2026 YoY (%)", color=bar_colors_2026, edgecolor="none", alpha=0.9, zorder=3)

ax.axhline(0, color="#374151", linewidth=1.1, zorder=2)

for rect in rects1:
    h = rect.get_height()
    va = "bottom" if h >= 0 else "top"
    y_pos = h + 1.8 if h >= 0 else h - 2.2
    ax.text(rect.get_x() + rect.get_width()/2, y_pos, f"{h:+.1f}%",
            ha="center", va=va, fontsize=10, fontweight="bold", color="#111827")

for rect in rects2:
    h = rect.get_height()
    va = "bottom" if h >= 0 else "top"
    y_pos = h + 1.8 if h >= 0 else h - 2.2
    ax.text(rect.get_x() + rect.get_width()/2, y_pos, f"{h:+.1f}%",
            ha="center", va=va, fontsize=10, fontweight="bold", color="#374151")

ax.annotate(
    "โตเร็วกว่า Shopee >2.3 เท่า\\nจากแรงหนุน Live & Affiliate",
    xy=(1 + width/2, 75.0), xytext=(1.38, 62.0),
    fontsize=9.5, fontweight="bold", color="#991B1B",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEF2F2", edgecolor=COLORS["TikTok Red"]),
    arrowprops=dict(arrowstyle="->", color=COLORS["TikTok Red"], lw=1.5)
)

ax.set_xticks(x)
ax.set_xticklabels(platforms, fontsize=11, fontweight="bold")
ax.set_ylabel("อัตราการเติบโตของ GMV (% YoY)", fontweight="bold")
ax.set_ylim(-42, 92)
ax.legend(loc="upper left")

chart_style.add_title_and_source(
    ax,
    title="TikTok Shop โตเร็วกว่า Shopee กว่า 2 เท่า (+53.4% vs +23.3% YoY) ขณะที่ Lazada หดตัว",
    subtitle="เปรียบเทียบอัตราการเติบโตของ GMV รายปี (2025 YoY) และโมเมนตัมต่อเนื่องใน H1 2026 (%)",
    source_text="Cube Asia (Tradewinds Dataset: USD 25.4B in 2024 -> USD 30.7B in 2025) & Momentum Works"
)

plt.savefig("../charts/01_2_growth_rate_comparison.png")
plt.show()"""
    ),
    new_markdown_cell(
        """> **Insight ของ Section 1:** *"Shopee ยังนำในภาพรวมปี 2025 แต่ trajectory ชี้ชัดว่ายุคแห่งการเป็นผู้นำเดี่ยว (Single-leader dominance) จบลงแล้วใน Q2 2026"*"""
    ),
]


# ==============================================================================
# NOTEBOOK 02: Threat Landscape
# ==============================================================================
nb02_cells = [
    new_markdown_cell(
        """# Section 2 — Threat Landscape: ศัตรูไม่ใช่ก้อนเดียว
**Business Question:** ภัยที่แท้จริงต่อ Shopee คือใคร และต่างกันอย่างไร?

### ข้อมูลที่ใช้ (Verified Public Data)
- **ข้อมูลงบการเงิน DBD (Baseline เปรียบเทียบโครงสร้างรายได้ vs กำไร/ขาดทุน):**
  - **Shopee (ประเทศไทย):** รายได้ 49,965 ล้านบาท | กำไรสุทธิ +4,631 ล้านบาท
  - **Lazada (ประเทศไทย):** รายได้ 28,291 ล้านบาท | กำไรสุทธิ +836 ล้านบาท
  - **TikTok Shop (ประเทศไทย):** รายได้ 12,066 ล้านบาท | **ขาดทุนสุทธิ -3,678 ล้านบาท** (ช่วงทุ่มงบอุดหนุนเพื่อแย่งชิงส่วนแบ่งตลาด)
- **ข้อมูล Temu:** เข้าไทย ก.ค. 2024 มียอดดาวน์โหลดสะสม >10 ล้านครั้ง (AppMagic) แต่ส่วนแบ่ง GMV ยัง <3% เน้นสินค้าราคาถูกส่งตรงจากโรงงานจีน"""
    ),
    new_code_cell(
        """import os
import pandas as pd
import matplotlib.pyplot as plt
import chart_style

chart_style.setup_plot_style()
COLORS = chart_style.COLORS

fin_df = pd.read_csv("../data/processed/sec02_competitor_financials.csv")
threat_df = pd.read_csv("../data/processed/sec02_threat_matrix.csv")
display(fin_df)
display(threat_df)"""
    ),
    new_markdown_cell(
        """### กราฟ 2.1 — Revenue vs Profit Scatter
- **สื่ออะไร:** TikTok Shop เติบโตอย่างก้าวกระโดดแต่แลกมาด้วยการเผาเงินขาดทุน (-3,678 ล้านบาท) ขณะที่ Shopee มีฐานกำไรที่แข็งแกร่ง (+4,631 ล้านบาท) ทำให้มี **Financial Runway** ที่เหนือกว่าหากไม่หลงลงไปเล่นสงครามเผาเงินเต็มรูปแบบ"""
    ),
    new_code_cell(
        """fig, ax = plt.subplots(figsize=(10.5, 6.0))

# Shaded loss zone below zero line
ax.axhspan(-5500, 0, color="#FEF2F2", alpha=0.6, zorder=1)
ax.axhline(0, color="#1F2937", linestyle="--", linewidth=1.5, zorder=2)
ax.text(1800, -480, "เส้นคุ้มทุน (Break-even Line = 0 บาท) | พื้นที่สีแดง = โซนขาดทุนสุทธิ",
        fontsize=9.5, fontweight="bold", color="#991B1B")

for _, row in fin_df.iterrows():
    plat = row["platform"]
    rev = row["revenue_mb"]
    prof = row["net_profit_mb"]
    gmv = row["gmv_usd_bn"]
    color = COLORS["TikTok Red"] if prof < 0 else COLORS.get(plat, COLORS["Grey"])
    size = gmv * 55

    ax.scatter(rev, prof, s=size, color=color, alpha=0.88, edgecolors="#111827", linewidths=1.8, zorder=4)

ax.annotate(
    "Shopee ประเทศไทย\\nรายได้: 49,965 ลบ. | กำไรสุทธิ: +4,631 ลบ.\\n(GMV USD 12.9B — มีกำไรเป็นเกราะป้องกัน)",
    xy=(49965, 4631), xytext=(28500, 4150),
    fontsize=10, fontweight="bold", color=COLORS["Shopee"],
    bbox=dict(boxstyle="round,pad=0.45", facecolor="#FFF7ED", edgecolor=COLORS["Shopee"], lw=1.3),
    arrowprops=dict(arrowstyle="->", color=COLORS["Shopee"], lw=1.6),
    zorder=5
)

ax.annotate(
    "Lazada ประเทศไทย\\nรายได้: 28,291 ลบ. | กำไรสุทธิ: +836 ลบ.\\n(GMV USD 5.2B — เน้นรักษา Margin / LazMall)",
    xy=(28291, 836), xytext=(7500, 1750),
    fontsize=9.5, fontweight="bold", color=COLORS["Lazada"],
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#EFF6FF", edgecolor=COLORS["Lazada"], lw=1.2),
    arrowprops=dict(arrowstyle="->", color=COLORS["Lazada"], lw=1.5),
    zorder=5
)

ax.annotate(
    "TikTok Shop ประเทศไทย\\nรายได้: 12,066 ลบ. | ขาดทุนสุทธิ: -3,678 ลบ.\\n(เผาเงินอุดหนุนคูปองและ Affiliate เพื่อเร่ง GMV)",
    xy=(12066, -3678), xytext=(17500, -4100),
    fontsize=10, fontweight="bold", color="#991B1B",
    bbox=dict(boxstyle="round,pad=0.45", facecolor="#FEF2F2", edgecolor=COLORS["TikTok Red"], lw=1.3),
    arrowprops=dict(arrowstyle="->", color=COLORS["TikTok Red"], lw=1.6),
    zorder=5
)

ax.set_xlabel("รายได้รวมในประเทศไทย (ล้านบาท)", fontweight="bold")
ax.set_ylabel("กำไร / ขาดทุนสุทธิ (ล้านบาท)", fontweight="bold")
ax.set_xlim(0, 58000)
ax.set_ylim(-5400, 6200)

chart_style.add_title_and_source(
    ax,
    title="TikTok Shop โตแรงแต่ขาดทุนหนัก (-3,678 ลบ.) ขณะที่ Shopee มีกำไรเป็นเกราะป้องกัน (+4,631 ลบ.)",
    subtitle="เปรียบเทียบรายได้รวม vs กำไร/ขาดทุนสุทธิ (ล้านบาท) และขนาดวงกลมตามสัดส่วน GMV (ปีฐาน DBD 2567)",
    source_text="กรมพัฒนาธุรกิจการค้า (DBD DataWarehouse+) / Creden Data & Cube Asia"
)

plt.savefig("../charts/02_1_revenue_vs_profit_scatter.png")
plt.show()"""
    ),
    new_markdown_cell(
        """### กราฟ 2.2 — Threat Positioning Matrix (2x2)
- **สื่ออะไร:** แยกแยะศัตรูตามระดับภัยคุกคามต่อ GMV และความยากในการตอบโต้ — **TikTok Shop** อยู่ใน Quadrant *"Structural Threat"* (ต้องจัดการเป็นลำดับแรก) ส่วน **Temu** เป็น *"Price Disruptor"* ที่ยังเล็กในแง่ GMV แต่กดดัน Margin ทั้งตลาด"""
    ),
    new_code_cell(
        """fig, ax = plt.subplots(figsize=(10.8, 6.4))

# Quadrant dividing lines at midpoint 5.0
ax.axvline(5.0, color="#6B7280", linestyle="--", linewidth=1.4, zorder=2)
ax.axhline(5.0, color="#6B7280", linestyle="--", linewidth=1.4, zorder=2)

# Subtle quadrant background shading
ax.fill_between([5.0, 10.5], 5.0, 10.5, color="#FEF2F2", alpha=0.5, zorder=1)
ax.fill_between([0.0, 5.0], 5.0, 10.5, color="#ECFDF5", alpha=0.45, zorder=1)
ax.fill_between([5.0, 10.5], 0.0, 5.0, color="#EFF6FF", alpha=0.4, zorder=1)
ax.fill_between([0.0, 5.0], 0.0, 5.0, color="#F9FAFB", alpha=0.6, zorder=1)

# Quadrant Header Labels placed cleanly at corners
ax.text(9.9, 9.85, "Q1: Structural Threat (ภัยเชิงโครงสร้าง - ต้องจัดการก่อน)",
        ha="right", va="top", fontsize=10, fontweight="bold", color="#991B1B",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFFFF", edgecolor="#FCA5A5"))
ax.text(0.3, 9.85, "Q2: Price Disruptor (ภัยกดดันราคาและ Margin ตลาด)",
        ha="left", va="top", fontsize=10, fontweight="bold", color="#065F46",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFFFF", edgecolor="#6EE7B7"))
ax.text(9.9, 0.35, "Q3: Traditional Rival (คู่แข่งโมเดลเดียวกัน - ป้องกันด้วยขนาด)",
        ha="right", va="bottom", fontsize=9.5, fontweight="bold", color="#1E40AF",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFFFF", edgecolor="#93C5FD"))
ax.text(0.3, 0.35, "Q4: Watchlist (ผู้เล่นเฉพาะกลุ่ม - เฝ้าระวัง)",
        ha="left", va="bottom", fontsize=9.5, fontweight="bold", color="#4B5563",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFFFF", edgecolor="#D1D5DB"))

color_map = {
    "TikTok Shop": COLORS["TikTok Shop"],
    "Temu": COLORS["Temu"],
    "Lazada": COLORS["Lazada"],
    "ผู้เล่น Local (NocNoc / Pantip Mall)": COLORS["Local"]
}

for _, row in threat_df.iterrows():
    comp = row["competitor"]
    x_val = row["gmv_threat_score"]
    y_val = row["counter_difficulty_score"]
    c = color_map.get(comp, COLORS["Grey"])

    ax.scatter(x_val, y_val, s=300, color=c, edgecolors="#FFFFFF", linewidths=2.0, zorder=5)

# Non-overlapping callouts inside each quadrant
ax.annotate(
    "TikTok Shop (GMV Share 48%)\\n- พฤติกรรม: Impulse / Discovery-led\\n- เปลี่ยนวิธีที่คนไทยค้นหาสินค้า",
    xy=(9.0, 8.4), xytext=(5.35, 6.1),
    fontsize=9.5, fontweight="bold", color="#111827",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFFFFF", edgecolor=COLORS["TikTok Shop"], lw=1.4),
    arrowprops=dict(arrowstyle="->", color=COLORS["TikTok Shop"], lw=1.5),
    zorder=6
)

ax.annotate(
    "Temu (GMV Share <3%, ดาวน์โหลด >10M)\\n- พฤติกรรม: สินค้าโรงงานจีนราคาถูกสุดขั้ว\\n- กดดัน Margin หมวด Non-brand",
    xy=(4.2, 6.8), xytext=(0.35, 7.3),
    fontsize=9.5, fontweight="bold", color=COLORS["Temu"],
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFFFFF", edgecolor=COLORS["Temu"], lw=1.4),
    arrowprops=dict(arrowstyle="->", color=COLORS["Temu"], lw=1.5),
    zorder=6
)

ax.annotate(
    "Lazada (GMV Share 7%)\\n- พฤติกรรม: Intent-based / LazMall\\n- โมเดลเหมือน Shopee ตอบโต้ได้ง่ายกว่า",
    xy=(5.8, 3.5), xytext=(5.6, 1.5),
    fontsize=9.5, fontweight="bold", color=COLORS["Lazada"],
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFFFFF", edgecolor=COLORS["Lazada"], lw=1.3),
    arrowprops=dict(arrowstyle="->", color=COLORS["Lazada"], lw=1.4),
    zorder=6
)

ax.annotate(
    "ผู้เล่น Local (เช่น NocNoc / Pantip Mall)\\n- เฉพาะกลุ่ม Vertical (GMV <1%)",
    xy=(2.2, 2.4), xytext=(0.35, 3.6),
    fontsize=9.5, fontweight="bold", color="#374151",
    bbox=dict(boxstyle="round,pad=0.35", facecolor="#FFFFFF", edgecolor=COLORS["Local"], lw=1.1),
    arrowprops=dict(arrowstyle="->", color=COLORS["Local"], lw=1.2),
    zorder=6
)

ax.set_xlabel("ระดับภัยคุกคามต่อส่วนแบ่ง GMV ของ Shopee (ต่ำ -> สูง)", fontweight="bold")
ax.set_ylabel("ความยากในการตอบโต้เชิงโครงสร้างของ Shopee (ต่ำ -> สูง)", fontweight="bold")
ax.set_xlim(0, 10.3)
ax.set_ylim(0, 10.4)

chart_style.add_title_and_source(
    ax,
    title="TikTok Shop คือภัยเชิงโครงสร้างอันดับ 1 ส่วน Temu คือตัวกดดัน Margin จากสินค้าราคาถูก",
    subtitle="เมทริกซ์จัดลำดับภัยคุกคาม (2x2 Threat Positioning Matrix) ประเมินจากขนาดผลกระทบ GMV และความยากในการสกัดกั้น",
    source_text="การประเมินเชิงกลยุทธ์จากข้อมูล Cube Asia, AppMagic (Temu >10M Downloads) และโครงสร้างพฤติกรรมผู้ซื้อ"
)

plt.savefig("../charts/02_2_threat_positioning_matrix.png")
plt.show()"""
    ),
    new_markdown_cell(
        """> **Insight ของ Section 2:** *"TikTok Shop คือภัยเชิงโครงสร้างที่ต้องจัดลำดับแรก เพราะดึงเวลาและเม็ดเงินผ่าน Impulse Commerce; ส่วน Temu เป็นภัยเชิงราคาที่ยังเล็กในแง่ GMV แต่กดดัน Margin ทั้งตลาด"*"""
    ),
]


# ==============================================================================
# NOTEBOOK 03: Internal Pressure
# ==============================================================================
nb03_cells = [
    new_markdown_cell(
        """# Section 3 — Internal Pressure: Shopee แบกอะไรอยู่
**Business Question:** Shopee มีทรัพยากรพอจะรบทุก Frontline หรือไม่?

### ข้อมูลที่ใช้ (Verified Public Data)
- **งบการเงิน บจก. ช้อปปี้ (ประเทศไทย) จาก DBD (ปี 2023–2025 / พ.ศ. 2566–2568):**
  - ปี 2023 (2566): รายได้ 29,476 ลบ. | กำไรสุทธิ 2,165 ลบ.
  - ปี 2024 (2567): รายได้ 49,964 ลบ. | กำไรสุทธิ 4,630 ลบ. (+113.9% YoY)
  - ปี 2025 (2568): รายได้ 88,387 ลบ. | กำไรสุทธิ **2,756 ลบ. (-40.5% YoY)**
- **โครงสร้างต้นทุนผู้ขาย & มาตรการลด GP กระทรวงพาณิชย์:**
  - ผู้ขายรายย่อยแบกต้นทุนรวม ~34.7% ของยอดขาย
  - กระทรวงพาณิชย์เจรจาปรับลดเพดาน GP ของ Shopee จาก **19.26%** เหลือ **8.03% – 13.91%**"""
    ),
    new_code_cell(
        """import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import chart_style

chart_style.setup_plot_style()
COLORS = chart_style.COLORS

trend_df = pd.read_csv("../data/processed/sec03_shopee_financial_trend.csv")
seller_df = pd.read_csv("../data/processed/sec03_seller_cost_burden.csv")
gp_df = pd.read_csv("../data/processed/sec03_gp_reduction.csv")
display(trend_df)
display(seller_df)
display(gp_df)"""
    ),
    new_markdown_cell(
        """### กราฟ 3.1 — Revenue vs Profit Trend (2023–2025)
- **สื่ออะไร:** รายได้ของ Shopee ประเทศไทยเติบโตก้าวกระโดดแตะ 88,387 ล้านบาทในปี 2025 แต่กำไรสุทธิกลับหดตัวลงถึง **-40.5%** (จาก 4,630 ลบ. เหลือ 2,756 ลบ.) สะท้อนถึงต้นทุนการเผาเงินอุดหนุนคูปองและ Live เพื่อต้านทานการรุกของ TikTok Shop"""
    ),
    new_code_cell(
        """fig, ax1 = plt.subplots(figsize=(10.2, 6.0))

x = np.arange(len(trend_df))
years = trend_df["year"].tolist()
revs = trend_df["revenue_mb"].tolist()
profits = trend_df["net_profit_mb"].tolist()

# Left axis: Revenue bars
bars = ax1.bar(x, revs, width=0.44, color="#FDBA74", edgecolor=COLORS["Shopee"], linewidth=1.5,
               label="รายได้รวม (ล้านบาท) - แกนซ้าย", zorder=3)
for i, b in enumerate(bars):
    h = b.get_height()
    y_pos = h + 1800 if i != 0 else h - 5500
    txt_col = "#9A3412" if i != 0 else "#7C2D12"
    ax1.text(b.get_x() + b.get_width()/2, y_pos, f"รายได้: {h:,.0f} ลบ.",
             ha="center", va="bottom", fontsize=10, fontweight="bold", color=txt_col)

ax1.set_xticks(x)
ax1.set_xticklabels(years, fontsize=11, fontweight="bold")
ax1.set_ylabel("รายได้รวม (ล้านบาท)", fontweight="bold", color="#9A3412")
ax1.set_ylim(0, 108000)

# Right axis: Net Profit line
ax2 = ax1.twinx()
ax2.grid(False)
ax2.spines["top"].set_visible(False)

line = ax2.plot(x, profits, color=COLORS["TikTok Red"], marker="o", markersize=10, linewidth=3.2,
                label="กำไรสุทธิ (ล้านบาท) - แกนขวา", zorder=5)

for i, p in enumerate(profits):
    offset = 320
    ax2.text(x[i], p + offset, f"กำไร: {p:,.0f} ลบ.",
             ha="center", va="bottom", fontsize=10, fontweight="bold", color="#991B1B",
             bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#FCA5A5"))

# Annotate -40.5% drop between 2024 and 2025
ax2.annotate(
    "กำไรสุทธิลดลง -40.5% YoY\\n(อัตรากำไรสุทธิลดจาก 9.3% -> 3.1%\\nจากการทุ่มงบสู้ศึกส่วนแบ่งตลาด)",
    xy=(2, 2756), xytext=(0.95, 1050),
    fontsize=10, fontweight="bold", color="#991B1B",
    bbox=dict(boxstyle="round,pad=0.45", facecolor="#FEF2F2", edgecolor=COLORS["TikTok Red"], lw=1.4),
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2", color=COLORS["TikTok Red"], lw=1.8),
    zorder=6
)

ax2.set_ylabel("กำไรสุทธิ (ล้านบาท)", fontweight="bold", color="#991B1B")
ax2.set_ylim(0, 6200)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

chart_style.add_title_and_source(
    ax1,
    title="รายได้ Shopee โตแตะ 88,387 ลบ. แต่กำไรสุทธิปี 2025 ร่วงลง -40.5% จากศึกเผาเงินรักษาส่วนแบ่ง",
    subtitle="แนวโน้มรายได้รวม (แท่ง) และกำไรสุทธิ (เส้น) ของ บจก. ช้อปปี้ (ประเทศไทย) ปี 2023-2025 (ล้านบาท)",
    source_text="กรมพัฒนาธุรกิจการค้า (DBD) งบการเงิน บจก. ช้อปปี้ (ประเทศไทย) ปี 2566-2568"
)

plt.savefig("../charts/03_1_revenue_vs_profit_trend.png")
plt.show()"""
    ),
    new_markdown_cell(
        """### กราฟ 3.2 — Seller Cost Burden Breakdown
- **สื่ออะไร:** ผู้ขายรายเล็กแบกต้นทุนรวมบนแพลตฟอร์มสูงถึง **34.7%** ของยอดขาย (เหลือกำไรสุทธิเพียง ~8%) หาก Shopee บีบเก็บค่าธรรมเนียมเพิ่มเพื่อชดเชยกำไรที่ลดลง จะเกิดความเสี่ยงที่ผู้ขายรายย่อยย้ายหนีออกจากระบบนิเวศ"""
    ),
    new_code_cell(
        """fig, ax = plt.subplots(figsize=(10.5, 6.0))

tiers = seller_df["seller_tier"].tolist()
x = np.arange(len(tiers))
width = 0.46

components = [
    ("commission_pct", "ค่าคอมมิชชัน (GP)", "#EE4D2D"),
    ("ads_pct", "ค่าโฆษณา (Shopee Ads)", "#F97316"),
    ("logistics_pct", "ต้นทุนโลจิสติกส์และการจัดส่ง", "#FBBF24"),
    ("promo_fee_pct", "ค่าธรรมเนียมโปรแกรมเสริม (ส่งฟรี/โค้ดคุ้ม)", "#60A5FA"),
    ("payment_fee_pct", "ค่าธุรกรรมการชำระเงิน (3.21%)", "#9CA3AF"),
]

bottom = np.zeros(len(tiers))
for col, label, color in components:
    vals = seller_df[col].values
    bars = ax.bar(x, vals, width, bottom=bottom, label=label, color=color, edgecolor="#FFFFFF", linewidth=0.8, zorder=3)
    for i, v in enumerate(vals):
        if v >= 3.0:
            ax.text(x[i], bottom[i] + v/2, f"{v:.1f}%", ha="center", va="center",
                    fontsize=9.5, fontweight="bold", color="#FFFFFF" if color in ["#EE4D2D", "#F97316"] else "#111827")
    bottom += vals

for i, tot in enumerate(seller_df["total_cost_pct"]):
    ax.text(x[i], tot + 1.0, f"ภาระต้นทุนรวม: {tot:.1f}%",
            ha="center", va="bottom", fontsize=10.5, fontweight="bold", color="#991B1B")

ax.plot(x, seller_df["seller_net_margin_pct"], color="#15803D", marker="D", markersize=9,
        linewidth=2.5, linestyle="--", label="กำไรสุทธิผู้ขายโดยประมาณ (% ของยอดขาย)", zorder=5)

for i, m in enumerate(seller_df["seller_net_margin_pct"]):
    ax.annotate(
        f"กำไรสุทธิร้านค้า ~{m:.1f}%",
        xy=(x[i], m), xytext=(x[i] + 0.27, m + 1.2),
        fontsize=9.5, fontweight="bold", color="#15803D",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#ECFDF5", edgecolor="#15803D"),
        arrowprops=dict(arrowstyle="->", color="#15803D", lw=1.2),
        zorder=6
    )

ax.set_xticks(x)
ax.set_xticklabels(tiers, fontsize=10.5, fontweight="bold")
ax.set_ylabel("สัดส่วนต่อยอดขายรวม (% of Gross Sales)", fontweight="bold")
ax.set_ylim(0, 44)
ax.set_xlim(-0.45, 2.75)
ax.legend(loc="upper right", fontsize=9.5)

chart_style.add_title_and_source(
    ax,
    title="ผู้ขายรายเล็กแบกต้นทุนแพลตฟอร์มสูงถึง 34.7% ของยอดขาย เหลือกำไรสุทธิเพียง ~8%",
    subtitle="โครงสร้างภาระต้นทุนผู้ขายบนแพลตฟอร์มแยกตามขนาดร้านค้า (% ของยอดขาย) เทียบกับกำไรสุทธิที่ผู้ขายได้รับจริง",
    source_text="Shopee Seller Centre Fee Schedule, FlowAccount E-Commerce Benchmark & การประเมินโครงสร้างต้นทุนผู้ขาย"
)

plt.savefig("../charts/03_2_seller_cost_burden.png")
plt.show()"""
    ),
    new_markdown_cell(
        """### กราฟ 3.3 — GP Reduction Impact (ก่อน/หลัง)
- **สื่ออะไร:** มาตรการของกระทรวงพาณิชย์กดดันให้ลดเพดาน GP สูงสุดจาก **19.26%** เหลือ **8.03% – 13.91%** (ลดลงสูงสุด -33.3%) ปิดทางไม่ให้ Shopee ขึ้นค่า GP กับร้านค้ารายย่อยเพื่อปั๊มกำไรระยะสั้น"""
    ),
    new_code_cell(
        """fig, ax = plt.subplots(figsize=(10.0, 5.6))

periods = gp_df["period"].tolist()
x = np.arange(len(periods))
width = 0.25

r_max = ax.bar(x - width, gp_df["max_gp_pct"], width, label="อัตรา GP เพดานสูงสุด (Max GP)", color=COLORS["Shopee"], zorder=3)
r_mid = ax.bar(x, gp_df["mid_gp_pct"], width, label="อัตรา GP หมวดสินค้าทั่วไป (Mid Tier)", color="#FB923C", zorder=3)
r_min = ax.bar(x + width, gp_df["min_gp_pct"], width, label="อัตรา GP ขั้นต่ำ (Min GP)", color="#FDBA74", zorder=3)

for bars in [r_max, r_mid, r_min]:
    for b in bars:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width()/2, h + 0.45, f"{h:.2f}%",
                ha="center", va="bottom", fontsize=10, fontweight="bold", color="#111827")

ax.annotate(
    "มาตรการรัฐกดเพดาน GP ลง\\n19.26% -> 8.03%-13.91%\\n(ลดภาระผู้ขายรายย่อยสูงสุด -33.3%)",
    xy=(1 - width, 13.91), xytext=(0.12, 19.8),
    fontsize=10, fontweight="bold", color="#991B1B",
    bbox=dict(boxstyle="round,pad=0.45", facecolor="#FEF2F2", edgecolor=COLORS["TikTok Red"], lw=1.3),
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2", color=COLORS["TikTok Red"], lw=1.8),
    zorder=5
)

ax.set_xticks(x)
ax.set_xticklabels(periods, fontsize=11, fontweight="bold")
ax.set_ylabel("อัตราค่าธรรมเนียมการขาย / GP (% รวม VAT)", fontweight="bold")
ax.set_ylim(0, 24.5)
ax.legend(loc="upper right")

chart_style.add_title_and_source(
    ax,
    title="มาตรการรัฐกดเพดาน GP ลงจาก 19.26% เหลือ 8.03-13.91% บีบให้ Shopee ต้องรัดเข็มขัดต้นทุน",
    subtitle="เปรียบเทียบอัตราค่าธรรมเนียมการขายภาคบังคับ (GP %) ก่อนและหลังมาตรการช่วยเหลือผู้ประกอบการ SME ของกระทรวงพาณิชย์",
    source_text="ประกาศกระทรวงพาณิชย์ / กรมประชาสัมพันธ์ (PRD) และฐานเศรษฐกิจ (มีผลกับผู้ขายรายย่อยกว่า 1.2 ล้านราย)"
)

plt.savefig("../charts/03_3_gp_reduction_impact.png")
plt.show()"""
    ),
    new_markdown_cell(
        """> **Insight ของ Section 3:** *"Shopee มีกำไรแต่กำลังบางลง (-40.5% YoY) ขณะที่ผู้ขายรายย่อยก็แบกต้นทุนหนักและรัฐคุมเพดาน GP — ทรัพยากรมีจำกัด จึงไม่สามารถเผาเงินรบทุกสมรภูมิพร้อมกันได้"*"""
    ),
]


# ==============================================================================
# NOTEBOOK 04: Regulatory Wind
# ==============================================================================
nb04_cells = [
    new_markdown_cell(
        """# Section 4 — Regulatory Wind: กฎระเบียบเปลี่ยนเกม
**Business Question:** กฎใหม่กระทบใครหนักกว่ากัน และ Shopee ใช้เป็นโอกาสได้ไหม?

### ข้อมูลที่ใช้ (Verified Public Data)
1. **มาตรการจัดเก็บ VAT 7% สินค้านำเข้า < 1,500 บาท (กรมสรรพากร/กรมศุลกากร):** เก็บ VAT 7% ตั้งแต่บาทแรกของราคา CIF (เริ่ม 5 ก.ค. 2567)
2. **แนวปฏิบัติ กขค. (TCCT Guideline 6 ด้าน):** คุมความโปร่งใสค่าธรรมเนียม, ห้ามบังคับใช้ขนส่งรายเดียวอย่างไม่เป็นธรรม, และกำกับอัลกอริทึม (Self-preferencing / Visibility blocking)
3. **โครงการ "OTOP ไทยโตไกลกับ Shopee" (กรมการพัฒนาชุมชน x Shopee):** ลดค่า GP เหลือเริ่มต้น **4.00%** + ยกเว้นค่าธรรมเนียมโครงสร้างพื้นฐาน + โบนัสเครดิตโฆษณา 50–100%"""
    ),
    new_code_cell(
        """import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import chart_style

chart_style.setup_plot_style()
COLORS = chart_style.COLORS

heat_df = pd.read_csv("../data/processed/sec04_regulatory_heatmap.csv")
cost_df = pd.read_csv("../data/processed/sec04_cost_shift.csv")
display(heat_df)
display(cost_df)"""
    ),
    new_markdown_cell(
        """### กราฟ 4.1 — Regulatory Impact Heatmap
- **สื่ออะไร:** ผู้ขาย Cross-border จากจีนและ Temu ได้รับผลกระทบหนักที่สุด (ระดับ 5/5) จากกำแพงภาษี VAT นำเข้าและมาตรการคุมมาตรฐานสินค้า ขณะที่ผู้ขายในประเทศและโครงการ OTOP ของ Shopee ได้รับอานิสงส์เชิงโครงสร้าง"""
    ),
    new_code_cell(
        """fig, ax = plt.subplots(figsize=(11.2, 6.0))

stakeholders = heat_df["stakeholder"].tolist()
measures = [
    "VAT สินค้านำเข้า <1,500฿\\n(เก็บ 7% ตั้งแต่บาทแรก)",
    "TCCT: ความโปร่งใสและ\\nเพดานค่าธรรมเนียม",
    "TCCT: ห้ามผูกขาดขนส่ง\\n(Logistics Choice)",
    "TCCT: กำกับอัลกอริทึม\\n& ป้องกันปิดกั้นการมองเห็น"
]
matrix = heat_df[["vat_import_1500", "tcct_fee_cap", "tcct_logistics", "tcct_algorithm"]].values

im = ax.imshow(matrix, cmap="Reds", vmin=0.5, vmax=5.3, aspect="auto")
ax.grid(False)

level_labels = {
    1: "1 (ได้เปรียบ/หนุน)",
    2: "2 (กระทบต่ำ)",
    3: "3 (ปานกลาง)",
    4: "4 (กระทบสูง)",
    5: "5 (กระทบหนักสุด)"
}

for i in range(len(stakeholders)):
    for j in range(len(measures)):
        val = matrix[i, j]
        txt_color = "#FFFFFF" if val >= 4 else "#111827"
        ax.text(j, i, level_labels[val], ha="center", va="center",
                fontsize=10, fontweight="bold", color=txt_color)

ax.set_xticks(np.arange(len(measures)))
ax.set_xticklabels(measures, fontsize=10, fontweight="bold")
ax.set_yticks(np.arange(len(stakeholders)))
ax.set_yticklabels(stakeholders, fontsize=10.5, fontweight="bold")

cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.03)
cbar.set_label("ระดับแรงกดดันเชิงลบจากกฎระเบียบ (1 = ต่ำ/ได้ประโยชน์ -> 5 = รุนแรงมาก)", fontsize=9.5, fontweight="bold")

chart_style.add_title_and_source(
    ax,
    title="กฎระเบียบใหม่กระทบผู้ขายจีนและ Temu หนักสุด (5/5) แต่เปิดทางให้ฐาน Local ของ Shopee ได้เปรียบ",
    subtitle="Heatmap ประเมินระดับผลกระทบจากมาตรการ VAT สินค้านำเข้าและแนวปฏิบัติ TCCT (กขค.) ต่อผู้เล่นแต่ละกลุ่ม",
    source_text="กรมสรรพากร/กรมศุลกากร (VAT 7% <1,500฿) และสำนักงานคณะกรรมการการแข่งขันทางการค้า (TCCT Guideline 6 ด้าน)"
)

plt.savefig("../charts/04_1_regulatory_impact_heatmap.png")
plt.show()"""
    ),
    new_markdown_cell(
        """### กราฟ 4.2 — Cost Shift Cross-border vs Local vs OTOP
- **สื่ออะไร:** ช่องว่างต้นทุนการขายระหว่างสินค้า Cross-border (พุ่งเป็น **25.5%**) กับสินค้า OTOP บน Shopee (ลดลงเหลือ **14.2%** ด้วยเรต GP 4%) ถ่างกว้างขึ้นถึง **11.3 percentage points** — กลายเป็นคูเมือง (Moat) ที่คู่แข่งจากจีนลอกเลียนแบบได้ยาก"""
    ),
    new_code_cell(
        """fig, ax = plt.subplots(figsize=(10.2, 5.8))

groups = cost_df["seller_group"].tolist()
x = np.arange(len(groups))
width = 0.35

before_vals = cost_df["cost_before_pct"].tolist()
after_vals = cost_df["cost_after_pct"].tolist()
deltas = cost_df["delta_pct"].tolist()

rects1 = ax.bar(x - width/2, before_vals, width, label="ก่อนมาตรการรัฐและโปรแกรม OTOP (%)", color="#9CA3AF", zorder=3)
after_colors = [COLORS["TikTok Red"], COLORS["Shopee"], COLORS["OTOP"]]
rects2 = ax.bar(x + width/2, after_vals, width, label="หลังมาตรการ VAT 7% / ลด GP / OTOP 4% (%)", color=after_colors, zorder=3)

for b in rects1:
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2, h + 0.5, f"{h:.1f}%",
            ha="center", va="bottom", fontsize=10, fontweight="bold", color="#4B5563")

for i, b in enumerate(rects2):
    h = b.get_height()
    d = deltas[i]
    sign_color = "#991B1B" if d > 0 else "#065F46"
    ax.text(b.get_x() + b.get_width()/2, h + 0.5, f"{h:.1f}%\\n({d:+.1f}%)",
            ha="center", va="bottom", fontsize=10, fontweight="bold", color=sign_color)

ax.annotate(
    "แต้มต่อต้นทุนถ่างออก 11.3 pp!\\n- Cross-border แพงขึ้นเป็น 25.5% (+VAT 7%)\\n- OTOP บน Shopee ลดเหลือ 14.2% (เรต GP 4%)",
    xy=(2 + width/2, 14.2), xytext=(1.02, 29.8),
    fontsize=10, fontweight="bold", color="#065F46",
    bbox=dict(boxstyle="round,pad=0.45", facecolor="#ECFDF5", edgecolor=COLORS["OTOP"], lw=1.4),
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2", color=COLORS["OTOP"], lw=1.8),
    zorder=5
)

ax.set_xticks(x)
ax.set_xticklabels(groups, fontsize=10.5, fontweight="bold")
ax.set_ylabel("ต้นทุนการขายรวมโดยประมาณ (% ของยอดขาย)", fontweight="bold")
ax.set_ylim(0, 36.5)
ax.legend(loc="upper left")

chart_style.add_title_and_source(
    ax,
    title="ส่วนต่างต้นทุนถ่างออก 11.3%: Cross-border แพงขึ้นจาก VAT 7% ขณะที่ OTOP บน Shopee ลดเหลือ 14.2%",
    subtitle="เปรียบเทียบภาระต้นทุนรวมของผู้ขาย (% ของยอดขาย) ก่อนและหลังมาตรการภาษีนำเข้าและโครงการ OTOP ไทยโตไกลกับ Shopee",
    source_text="กรมศุลกากร (VAT 7%), กระทรวงพาณิชย์ และโครงการ OTOP ไทยโตไกลกับ Shopee (พช. กระทรวงมหาดไทย)"
)

plt.savefig("../charts/04_2_cost_shift_comparison.png")
plt.show()"""
    ),
    new_markdown_cell(
        """> **Insight ของ Section 4:** *"กฎระเบียบใหม่ไม่ใช่แค่ความเสี่ยงด้านค่าธรรมเนียม แต่เป็นลมหนุนสำคัญที่ทำให้ Moat ของ Shopee (ผู้ขายในประเทศ + OTOP เรต 4% + เครือข่าย SPX Express) มีความได้เปรียบเชิงต้นทุนเหนือสินค้านำเข้าชัดเจน"*"""
    ),
]


# ==============================================================================
# NOTEBOOK 05: Strategic Options
# ==============================================================================
nb05_cells = [
    new_markdown_cell(
        """# Section 5 — Strategic Options: ควรทำอะไรก่อน
**Business Question:** ในบรรดาทางเลือกเชิงกลยุทธ์ มีทางไหนคุ้มค่าที่สุดเมื่อเทียบกับขีดความสามารถจริงของ Shopee?

### ทางเลือกเชิงกลยุทธ์ 4 ทาง (4 Strategic Options)
1. **(1) Protect Intent-based Base:** ป้องกันฐานผู้ซื้อที่ตั้งใจค้นหาสินค้า (Search / Shopee Mall / การจัดส่งไวผ่าน SPX Express)
2. **(2) Selective Shoppertainment / Affiliate:** ลงทุน Live & Affiliate เฉพาะหมวดสินค้าที่ Margin สูง (ไม่เผาเงินหว่านทุกหมวดแข่งกับ TikTok)
3. **(3) Regulatory Tailwind / OTOP Moat:** ใช้ลมหนุนกฎหมายใหม่ ดึงผู้ขายไทยและ OTOP (เรต 4%) เข้าแพลตฟอร์มเพื่อสร้างสินค้า Exclusive ท้องถิ่น
4. **(4) Full-scale Quick Commerce:** ทุ่มงบเปิดศึกส่งด่วนระดับชั่วโมงเต็มรูปแบบแข่งกับแพลตฟอร์มเดลิเวอรีและร้านสะดวกซื้อ"""
    ),
    new_code_cell(
        """import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import chart_style

chart_style.setup_plot_style()
COLORS = chart_style.COLORS

opt_df = pd.read_csv("../data/processed/sec05_strategic_options.csv")
scen_df = pd.read_csv("../data/processed/sec05_scenarios.csv")
display(opt_df)
display(scen_df)"""
    ),
    new_markdown_cell(
        """### กราฟ 5.1 — Impact vs Feasibility Matrix (Bubble 2x2)
- **สื่ออะไร:** ทางเลือก **(1) ป้องกันฐาน Intent-based** และ **(3) ขยายฐาน Local/OTOP รับลมหนุนรัฐ** อยู่ใน Quadrant *"โอกาสสูง + ทำได้จริง"* โดยใช้งบลงทุนต่ำกว่าและมีความเสี่ยงต่ำกว่า ขณะที่ **(4) Quick Commerce** ใช้เงินทุนมหาศาลแต่มีความเป็นไปได้ต่ำและเสี่ยงสูง"""
    ),
    new_code_cell(
        """fig, ax = plt.subplots(figsize=(10.8, 6.4))

ax.axvline(5.5, color="#6B7280", linestyle="--", linewidth=1.4, zorder=2)
ax.axhline(5.5, color="#6B7280", linestyle="--", linewidth=1.4, zorder=2)

ax.fill_between([5.5, 10.3], 5.5, 10.3, color="#ECFDF5", alpha=0.5, zorder=1)
ax.fill_between([0.0, 5.5], 5.5, 10.3, color="#FEF2F2", alpha=0.45, zorder=1)
ax.fill_between([5.5, 10.3], 0.0, 5.5, color="#F9FAFB", alpha=0.5, zorder=1)
ax.fill_between([0.0, 5.5], 0.0, 5.5, color="#F3F4F6", alpha=0.5, zorder=1)

ax.text(10.0, 10.0, "Prioritize Now (โอกาสสูง + ทำได้จริง - โฟกัสทรัพยากรหลัก)",
        ha="right", va="top", fontsize=10, fontweight="bold", color="#065F46",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFFFF", edgecolor="#6EE7B7"))
ax.text(0.3, 10.0, "High Risk / Capital Trap (โอกาสมีแต่ทำยาก/เผาเงินสูง)",
        ha="left", va="top", fontsize=10, fontweight="bold", color="#991B1B",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFFFF", edgecolor="#FCA5A5"))

risk_colors = {
    1: COLORS["Shopee"],
    2: "#F59E0B",
    3: COLORS["OTOP"],
    4: COLORS["TikTok Red"]
}

for _, row in opt_df.iterrows():
    oid = int(row["option_id"])
    fx = row["feasibility_score"]
    iy = row["impact_score"]
    inv = row["investment_mb"]
    c = risk_colors[oid]

    ax.scatter(fx, iy, s=inv * 0.42, color=c, alpha=0.85, edgecolors="#111827", linewidths=2.0,
               label=f'{row["option_name"]} | งบ ~{inv:,} ลบ. ({row["risk_label"]})', zorder=4)
    ax.text(fx, iy, f"({oid})", ha="center", va="center", fontsize=11, fontweight="bold", color="#FFFFFF", zorder=5)

ax.annotate(
    "(1) ป้องกันฐาน Intent-based (Search + Mall + SPX)\\n- โอกาสสูงสุด (8.8) & ทำได้ทันทีด้วยสินทรัพย์เดิม",
    xy=(8.5, 8.8), xytext=(3.8, 8.65),
    fontsize=9.0, fontweight="bold", color="#9A3412",
    bbox=dict(boxstyle="round,pad=0.35", facecolor="#FFF7ED", edgecolor=COLORS["Shopee"]),
    arrowprops=dict(arrowstyle="->", color=COLORS["Shopee"], lw=1.5),
    zorder=6
)

ax.annotate(
    "(3) ใช้กฎรัฐปั้น OTOP 4% & Local SME\\n- ลงทุนต่ำสุด (~850 ลบ.) ความเสี่ยงต่ำ",
    xy=(8.8, 7.9), xytext=(6.65, 5.95),
    fontsize=9.0, fontweight="bold", color="#065F46",
    bbox=dict(boxstyle="round,pad=0.35", facecolor="#ECFDF5", edgecolor=COLORS["OTOP"]),
    arrowprops=dict(arrowstyle="->", color=COLORS["OTOP"], lw=1.5),
    zorder=6
)

ax.annotate(
    "(2) Selective Shoppertainment / Affiliate\\n- เจาะเฉพาะหมวด Margin สูง",
    xy=(7.0, 7.6), xytext=(4.2, 6.8),
    fontsize=9.0, fontweight="bold", color="#92400E",
    bbox=dict(boxstyle="round,pad=0.35", facecolor="#FFFBEB", edgecolor="#F59E0B"),
    arrowprops=dict(arrowstyle="->", color="#F59E0B", lw=1.5),
    zorder=6
)

ax.annotate(
    "(4) รุก Quick Commerce เต็มรูปแบบ\\n- ต้องใช้งบสูง ~3,500 ลบ. แข่งกับ 7-Eleven/Grab\\n- เสี่ยงขาดทุนซ้ำรอย",
    xy=(3.4, 6.4), xytext=(0.25, 7.6),
    fontsize=9.0, fontweight="bold", color="#991B1B",
    bbox=dict(boxstyle="round,pad=0.35", facecolor="#FEF2F2", edgecolor=COLORS["TikTok Red"]),
    arrowprops=dict(arrowstyle="->", color=COLORS["TikTok Red"], lw=1.5),
    zorder=6
)

ax.set_xlabel("ความเป็นไปได้ในการลงมือทำจริง / Execution Feasibility (ต่ำ -> สูง)", fontweight="bold")
ax.set_ylabel("ขนาดผลกระทบเชิงธุรกิจ / Business Impact (ต่ำ -> สูง)", fontweight="bold")
ax.set_xlim(0, 10.3)
ax.set_ylim(3.4, 10.4)
ax.legend(loc="lower left", fontsize=8.8, markerscale=0.32, labelspacing=0.6,
          title="ทางเลือกเชิงกลยุทธ์ (ขนาดวงกลม = งบลงทุนที่ต้องใช้)", title_fontsize=9.2)

chart_style.add_title_and_source(
    ax,
    title="ทางเลือก (1) ป้องกันฐาน Intent และ (3) รุก OTOP ให้ผลลัพธ์สูงและทำได้จริง ส่วน Quick Commerce เสี่ยงสูง",
    subtitle="Impact vs Feasibility Matrix (ขนาดวงกลมแสดงงบลงทุน, สีแสดงระดับความเสี่ยงในการดำเนินงาน 18 เดือน)",
    source_text="การประเมินทางเลือกเชิงกลยุทธ์ (BD Assessment Matrix) บนฐานโครงสร้างต้นทุนและสินทรัพย์ของ Shopee ประเทศไทย"
)

plt.savefig("../charts/05_1_impact_vs_feasibility_matrix.png")
plt.show()"""
    ),
    new_markdown_cell(
        """### กราฟ 5.2 — Scenario Comparison (Best / Base / Worst Case)
- **สื่ออะไร:** เปรียบเทียบความไม่แน่นอนของผลตอบแทนใน 18 เดือน — ทางเลือก (1) และ (3) ให้ผลตอบแทนเป็นบวกแม้ในกรณีเลวร้ายที่สุด (Worst Case +12.0% และ +10.5%) ในขณะที่ Quick Commerce มีโอกาสติดลบหนักถึง **-18.0%**"""
    ),
    new_code_cell(
        """fig, ax = plt.subplots(figsize=(10.2, 5.8))

options = scen_df["option_label"].tolist()
x = np.arange(len(options))
width = 0.25

r_best = ax.bar(x - width, scen_df["best_case_pct"], width, label="Best Case (กรณีดีที่สุด)", color="#16A34A", zorder=3)
r_base = ax.bar(x, scen_df["base_case_pct"], width, label="Base Case (กรณีฐานที่คาดหวัง)", color=COLORS["Shopee"], zorder=3)
r_worst = ax.bar(x + width, scen_df["worst_case_pct"], width, label="Worst Case (กรณีเลวร้ายที่สุด)", color="#DC2626", zorder=3)

ax.axhline(0, color="#1F2937", linewidth=1.2, zorder=2)

for bars in [r_best, r_base, r_worst]:
    for b in bars:
        h = b.get_height()
        va = "bottom" if h >= 0 else "top"
        offset = 0.9 if h >= 0 else -1.2
        ax.text(b.get_x() + b.get_width()/2, h + offset, f"{h:+.1f}%",
                ha="center", va=va, fontsize=9.5, fontweight="bold", color="#111827")

ax.annotate(
    "Downside Risk สูง (-18.0%)\\nหากเกิดสงครามราคาส่งด่วน",
    xy=(3 + width, -18.0), xytext=(2.05, -15.5),
    fontsize=9.5, fontweight="bold", color="#991B1B",
    bbox=dict(boxstyle="round,pad=0.35", facecolor="#FEF2F2", edgecolor="#DC2626"),
    arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.4)
)

ax.set_xticks(x)
ax.set_xticklabels(options, fontsize=10.5, fontweight="bold")
ax.set_ylabel("ดัชนีผลตอบแทนสุทธิคาดหวังใน 18 เดือน (Expected ROI %)", fontweight="bold")
ax.set_ylim(-25, 39)
ax.legend(loc="upper right")

chart_style.add_title_and_source(
    ax,
    title="การป้องกันฐานเดิมและใช้ลมหนุนรัฐให้ผลตอบแทนเป็นบวกแม้ใน Worst Case ต่างจาก Quick Commerce ที่เสี่ยงติดลบ",
    subtitle="เปรียบเทียบผลตอบแทนคาดหวังใน 18 เดือนแยกตามสถานการณ์ (Best Case / Base Case / Worst Case)",
    source_text="แบบจำลองสถานการณ์ (Scenario Modeling) จากสมมติฐานงบลงทุนและอัตรากำไรของ Shopee ประเทศไทย"
)

plt.savefig("../charts/05_2_scenario_comparison.png")
plt.show()"""
    ),
    new_markdown_cell(
        """> **Insight ของ Section 5:** *"การเผาเงินแข่ง Shoppertainment แบบปูพรมหรือเปิดศึก Quick Commerce ให้ ROI ต่ำกว่าและเสี่ยงกว่าการป้องกันฐาน Intent-based เดิมควบคู่กับการใช้ลมหนุนภาครัฐ (OTOP 4%)"*"""
    ),
]


# ==============================================================================
# NOTEBOOK 06: Recommendation & Memo
# ==============================================================================
nb06_cells = [
    new_markdown_cell(
        """# Section 6 — Recommendation & Memo: สรุปแผนปฏิบัติการ 18 เดือน
**Business Question:** แล้วสรุป Shopee ควรทำอะไร และจัดลำดับความสำคัญอย่างไร?

### ข้อเสนอแนะ 3 เสาหลัก (3 Strategic Pillars)
1. **Priority 1 (เดือนที่ 0–12): ป้องกันฐาน Intent-based + ยกระดับ SPX Express** — ล็อกกลุ่มลูกค้าที่ตั้งใจซื้อ (Search & Shopee Mall) ด้วยการการันตีความเร็วจัดส่งและคุณภาพสินค้าที่ TikTok Shop ทำตามได้ยาก
2. **Priority 2 (เดือนที่ 2–14): เปลี่ยนกฎรัฐเป็น Moat (ปั้น OTOP 4% + Local SME)** — ดึงผู้ผลิตไทยและสินค้า OTOP เข้าแพลตฟอร์มด้วยเรต GP 4% สร้างความได้เปรียบด้านราคาเหนือสินค้า Cross-border ที่โดน VAT 7%
3. **Priority 3 (เดือนที่ 4–18): รุก Affiliate & Live แบบเจาะจงหมวด Margin สูง** — ใช้งบอุดหนุนเฉพาะหมวด Beauty, Fashion และ Personal Care ที่มีกำไรสูง เพื่อหยุดการรั่วไหลของลูกค้าโดยไม่ทำลายบรรทัดสุดท้าย (Bottom-line)"""
    ),
    new_code_cell(
        """import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import chart_style

chart_style.setup_plot_style()
COLORS = chart_style.COLORS

rec_df = pd.read_csv("../data/processed/sec06_roadmap_and_impact.csv")
display(rec_df)"""
    ),
    new_markdown_cell(
        """### กราฟ 6.1 — Priority Roadmap (Gantt Timeline 0–18 Months)
- **สื่ออะไร:** ลำดับการลงมือทำอย่างเป็นระบบใน 18 เดือน เริ่มจากการล็อกฐานกำไรเดิมทันทีในเดือนแรก ตามด้วยการขยายฐานร้านค้าไทยรับกฎหมายใหม่ และการทำ Selective Attack ในฝั่ง Creator Affiliate"""
    ),
    new_code_cell(
        """fig, ax = plt.subplots(figsize=(10.5, 5.4))

df_plot = rec_df.iloc[::-1].reset_index(drop=True)
y_pos = np.arange(len(df_plot))

bar_colors = ["#F59E0B", COLORS["OTOP"], COLORS["Shopee"]]
milestones = [
    "M4-M18: โฟกัส Affiliate เฉพาะหมวด Margin สูง (คุมเพดาน Subsidy)",
    "M2-M14: ดึงร้าน OTOP (GP 4%) & SME ไทย ทดแทนสินค้าจีนที่โดน VAT 7%",
    "M0-M12: ล็อกฐาน Shopee Mall + ยกระดับ Next-Day Delivery ของ SPX Express"
]

for i, row in df_plot.iterrows():
    ax.barh(
        i, row["duration_months"], left=row["start_month"], height=0.48,
        color=bar_colors[i], edgecolor="#111827", linewidth=1.2, alpha=0.92,
        label=row["priority_level"], zorder=3
    )
    ax.text(
        row["start_month"] + 0.35, i, milestones[i],
        ha="left", va="center", fontsize=9.5, fontweight="bold",
        color="#FFFFFF" if i != 0 else "#111827", zorder=4
    )

for m, p_label in [(6, "ระยะที่ 1: Stabilize Core (M0-6)"), (12, "ระยะที่ 2: Scale Local Moat (M6-12)"), (18, "ระยะที่ 3: Harvest Margin (M12-18)")]:
    ax.axvline(m, color="#6B7280", linestyle=":", linewidth=1.2, zorder=2)
    ax.text(m - 3, 2.52, p_label, ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#374151",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#F3F4F6", edgecolor="#D1D5DB"))

ax.set_yticks(y_pos)
ax.set_yticklabels(df_plot["rec_title"], fontsize=10.5, fontweight="bold")
ax.set_xlabel("กรอบเวลาดำเนินงาน (เดือนที่ 0 ถึง เดือนที่ 18)", fontweight="bold")
ax.set_xticks(range(0, 19, 2))
ax.set_xticklabels([f"เดือน {m}" for m in range(0, 19, 2)])
ax.set_xlim(0, 18.8)
ax.set_ylim(-0.55, 2.95)
ax.legend(loc="upper right", bbox_to_anchor=(0.99, 0.84))

chart_style.add_title_and_source(
    ax,
    title="โรดแมป 18 เดือน: ล็อกฐานหลักทันที (M0-12) ควบคู่ปั้น OTOP Moat (M2-14) และเจาะ Affiliate เฉพาะจุด",
    subtitle="แผนผังลำดับการดำเนินงานเชิงกลยุทธ์ (Priority Execution Roadmap) แบ่งตาม 3 ระยะเวลาใน 18 เดือนข้างหน้า",
    source_text="แผนปฏิบัติการเชิงกลยุทธ์ (Shopee Thailand 18-Month BD Action Plan)"
)

plt.savefig("../charts/06_1_priority_roadmap.png")
plt.show()"""
    ),
    new_markdown_cell(
        """### กราฟ 6.2 — Expected Impact Summary
- **สื่ออะไร:** สรุปเปรียบเทียบผลกระทบคาดหวัง (Expected Impact Index) ของทั้ง 3 ข้อเสนอแนะให้เห็นชัดเจนใน 3 วินาที พร้อม KPI หลักที่ใช้ติดตามผล"""
    ),
    new_code_cell(
        """fig, ax = plt.subplots(figsize=(10.2, 5.2))

df_imp = rec_df.sort_values("expected_impact_index", ascending=True).reset_index(drop=True)
y_pos = np.arange(len(df_imp))
colors = ["#F59E0B", COLORS["OTOP"], COLORS["Shopee"]]

bars = ax.barh(y_pos, df_imp["expected_impact_index"], height=0.5, color=colors, edgecolor="#111827", linewidth=1.2, zorder=3)

for i, b in enumerate(bars):
    w = b.get_width()
    kpi = df_imp.loc[i, "key_kpi"]
    ax.text(w + 1.5, b.get_y() + b.get_height()/2, f"Impact Index: {w}/100\\n(KPI: {kpi})",
            ha="left", va="center", fontsize=9.5, fontweight="bold", color="#111827")

ax.set_yticks(y_pos)
ax.set_yticklabels(df_imp["rec_title"], fontsize=10.5, fontweight="bold")
ax.set_xlabel("ดัชนีผลกระทบเชิงกลยุทธ์ที่คาดหวัง (Expected Strategic Impact Index: 0-100)", fontweight="bold")
ax.set_xlim(0, 132)
ax.set_ylim(-0.55, 2.65)

chart_style.add_title_and_source(
    ax,
    title="การปกป้องฐาน Intent-based และ SPX Express สร้าง Impact สูงสุด (92/100) ต่อความอยู่รอดใน 18 เดือน",
    subtitle="เปรียบเทียบดัชนีผลกระทบคาดหวัง (Expected Impact Index) และตัวชี้วัดหลัก (Key KPIs) ของข้อเสนอแนะทั้ง 3 ข้อ",
    source_text="การประเมินผลกระทบเชิงกลยุทธ์ถ่วงน้ำหนัก (Weighted Impact Assessment — Shopee BD Memo)"
)

plt.savefig("../charts/06_2_expected_impact_summary.png")
plt.show()"""
    ),
    new_markdown_cell(
        """> **Insight ของ Section 6:** *"คำตอบของ Shopee ในอีก 18 เดือนไม่ใช่การเผาเงินแลก GMV ทุกสมรภูมิ แต่คือการจัดสรรทรัพยากรแบบ 50 : 30 : 20 — 50% ปกป้องฐาน Intent & SPX Express, 30% เปลี่ยนกฎรัฐเป็น OTOP/Local Moat, และ 20% เจาะ Selective Affiliate เฉพาะหมวดกำไรสูง"*"""
    ),
]


if __name__ == "__main__":
    build_and_run_notebook("01_market_shift.ipynb", nb01_cells)
    build_and_run_notebook("02_threat_landscape.ipynb", nb02_cells)
    build_and_run_notebook("03_internal_pressure.ipynb", nb03_cells)
    build_and_run_notebook("04_regulatory_wind.ipynb", nb04_cells)
    build_and_run_notebook("05_strategic_options.ipynb", nb05_cells)
    build_and_run_notebook("06_recommendation.ipynb", nb06_cells)
    print("All 6 notebooks and 13 charts generated successfully!")
