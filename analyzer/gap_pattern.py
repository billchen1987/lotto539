# 📦 匯入模組
import sqlite3
from pathlib import Path
from collections import Counter

# 📁 全域變數
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lotto539.db"

# 📐 分析間距模式
def analyze_gap_patterns():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        rows = cursor.fetchall()

    all_gaps = []

    for row in rows:
        sorted_nums = sorted(row)
        gaps = [sorted_nums[i + 1] - sorted_nums[i] for i in range(len(sorted_nums) - 1)]
        all_gaps.extend(gaps)

    gap_counter = Counter(all_gaps)
    return dict(sorted(gap_counter.items()))

# 🚀 主程式
if __name__ == "__main__":
    print("📐 今彩539 號碼間距模式分析")
    print("=" * 35)

    gap_stats = analyze_gap_patterns()
    print("📊 各間距出現次數：")
    for gap, count in gap_stats.items():
        print(f"間距 {gap:2d} ➜ {count} 次")
