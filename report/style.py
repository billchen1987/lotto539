# 📦 匯入模組
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 🖋️ 全域視覺樣式設定
# style.py

def apply_global_matplotlib_style():
    matplotlib.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Microsoft JhengHei", "Arial Unicode MS", "sans-serif"],  # or other CJK font
        "axes.unicode_minus": False,
        "font.size": 12,
        "axes.titlesize": 16,
        "axes.labelsize": 14,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 12,
        "figure.titlesize": 18,
        "axes.grid": True,
        "grid.linestyle": "--",
        "grid.alpha": 0.4
    })


# 🎨 主題色（可供圖表或報表使用）
COLOR_THEME = {
    "primary": "#4A90E2",
    "secondary": "#50E3C2",
    "highlight": "#F5A623",
    "text": "#333333",
    "background": "#F9F9F9"
}

# 🏷️ PDF標題風格建議（供 fpdf 使用時搭配）
PDF_STYLE = {
    "title_font": "Arial",
    "title_size": 16,
    "section_font": "Arial",
    "section_size": 14,
    "body_font": "Arial",
    "body_size": 12
}

# 📌 測試入口（可略）
if __name__ == "__main__":
    apply_global_matplotlib_style()
    print("✅ 已套用全域 matplotlib 樣式")
