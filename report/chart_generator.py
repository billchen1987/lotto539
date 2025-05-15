# 📦 匯入模組
import sqlite3
from collections import Counter
from pathlib import Path
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from style import apply_global_matplotlib_style
apply_global_matplotlib_style()

# 📁 全域變數
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lotto539.db"
IMG_DIR = BASE_DIR / "charts"
IMG_DIR.mkdir(exist_ok=True)

# 🔥 熱號柱狀圖
def generate_hot_number_chart(top_n=10):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        numbers = [n for row in cursor.fetchall() for n in row]

    counter = Counter(numbers).most_common(top_n)
    labels, values = zip(*counter)

    plt.figure()
    plt.bar(labels, values)
    plt.title("熱門號碼（前十）")
    plt.xlabel("號碼")
    plt.ylabel("出現次數")
    plt.tight_layout()
    plt.savefig(IMG_DIR / "hot_numbers.png")
    plt.close()

# 🧠 尾數分布圖
def generate_tail_digit_chart():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        numbers = [n for row in cursor.fetchall() for n in row]

    tails = [n % 10 for n in numbers]
    counter = Counter(tails)
    labels, values = zip(*sorted(counter.items()))

    plt.figure()
    plt.bar(labels, values)
    plt.title("尾數分布")
    plt.xlabel("尾數 (0~9)")
    plt.ylabel("出現次數")
    plt.tight_layout()
    plt.savefig(IMG_DIR / "tail_digits.png")
    plt.close()

# 📊 區間分布圖
def generate_range_segment_chart():
    def segment(num):
        if 1 <= num <= 10: return "01–10"
        if 11 <= num <= 20: return "11–20"
        if 21 <= num <= 30: return "21–30"
        if 31 <= num <= 39: return "31–39"

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        numbers = [n for row in cursor.fetchall() for n in row]

    segment_counter = Counter(segment(n) for n in numbers)
    labels, values = zip(*segment_counter.items())

    plt.figure()
    plt.bar(labels, values)
    plt.title("號碼區間分布")
    plt.xlabel("區間")
    plt.ylabel("出現次數")
    plt.tight_layout()
    plt.savefig(IMG_DIR / "range_segments.png")
    plt.close()

# ⚖️ 奇偶比例圓餅圖
def generate_odd_even_pie_chart():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        numbers = [n for row in cursor.fetchall() for n in row]

    odd = sum(1 for n in numbers if n % 2 == 1)
    even = sum(1 for n in numbers if n % 2 == 0)

    plt.figure()
    plt.pie([odd, even], labels=["奇數", "偶數"], autopct='%1.1f%%', startangle=140)
    plt.title("奇偶數比例")
    plt.axis("equal")
    plt.savefig(IMG_DIR / "odd_even_ratio.png")
    plt.close()

# 🚀 主程式
if __name__ == "__main__":
    print("📊 產生圖表中...")

    generate_hot_number_chart()
    generate_tail_digit_chart()
    generate_range_segment_chart()
    generate_odd_even_pie_chart()

    print(f"✅ 所有圖表已儲存至：{IMG_DIR}")
