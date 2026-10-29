"""Shared Matplotlib Design Rules & Brand Theme for Shopee BD Assessment.

Enforces Section 9 of project_doc_shopee.md:
- 1 Chart = 1 Insight (Insight-driven title)
- Consistent brand color palette across the entire project:
  Shopee = Orange (#EE4D2D)
  TikTok Shop = Black/Red (#111111 / #FE2C55)
  Lazada = Blue (#0F146D)
  Temu = Green (#2E8B57)
- Combined Latin + Thai typography via Noto Sans Thai Combined
- High-resolution 300 DPI export to charts/
"""

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Brand Color Palette (Section 9)
COLORS = {
    "Shopee": "#EE4D2D",         # Shopee Official Orange
    "TikTok Shop": "#111111",    # TikTok Black
    "TikTok Red": "#FE2C55",     # TikTok Crimson Red (used for loss / alert highlights)
    "Lazada": "#0F146D",         # Lazada Deep Royal Blue
    "Temu": "#2E8B57",           # Temu Sea Green (as specified in Section 9: Temu = เขียว)
    "Local": "#6C757D",          # Neutral Slate Grey for Local / Others
    "OTOP": "#198754",           # Emerald Green for OTOP / Tailwind
    "Grey": "#8C959F",
    "LightGrey": "#E9ECEF",
    "DarkText": "#1F2328",
}

def setup_plot_style():
    """Configure Matplotlib to render combined Latin + Thai text cleanly."""
    here = os.path.dirname(os.path.abspath(__file__))
    font_dir = os.path.join(here, "fonts")
    if os.path.exists(font_dir):
        for fname in os.listdir(font_dir):
            if fname.endswith(".ttf"):
                fm.fontManager.addfont(os.path.join(font_dir, fname))

    plt.rcParams.update({
        "font.family": "Noto Sans Thai Combined",
        "axes.unicode_minus": False,
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
        "axes.edgecolor": "#CCCCCC",
        "axes.linewidth": 0.9,
        "axes.grid": True,
        "grid.color": "#E5E7EB",
        "grid.linestyle": "--",
        "grid.linewidth": 0.7,
        "grid.alpha": 0.7,
        "xtick.color": "#333333",
        "ytick.color": "#333333",
        "xtick.labelsize": 10.5,
        "ytick.labelsize": 10.5,
        "axes.labelsize": 11.5,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "legend.frameon": True,
        "legend.facecolor": "#FFFFFF",
        "legend.edgecolor": "#E5E7EB",
        "legend.fontsize": 10.0,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.25,
    })

def add_title_and_source(ax, title, subtitle=None, source_text=None):
    """Apply insight title, optional subtitle, and bottom source citation."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if subtitle:
        ax.set_title(f"{title}\n", fontsize=14.0, fontweight="bold", loc="left", color="#111827", pad=16)
        ax.text(
            0.0, 1.02, subtitle,
            transform=ax.transAxes,
            fontsize=10.5, color="#4B5563",
            ha="left", va="bottom"
        )
    else:
        ax.set_title(title, fontsize=14.0, fontweight="bold", loc="left", color="#111827", pad=14)

    if source_text:
        ax.text(
            0.0, -0.15, f"แหล่งข้อมูล (Source): {source_text}",
            transform=ax.transAxes,
            fontsize=9, color="#6B7280",
            ha="left", va="top"
        )
