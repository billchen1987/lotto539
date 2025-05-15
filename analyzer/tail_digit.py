# 📦 匯入模組
import sqlite3
from collections import Counter
from pathlib import Path

# 📁 全域設定
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lotto539.db"

# 🔢 尾數分析
def analyze_tail_digits():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        all_numbers = [n for row in cursor.fetchall() for n in row]

    tail_digits = [n % 10 for n in all_numbers]
    tail_counter = Counter(tail_digits)

    return sorted(tail_counter.items())  # 依照尾數 0~9 排序輸出

# 🚀 主程式
if __name__ == "__main__":
    print("🔢 今彩539 尾數分析（0~9）")
    print("=" * 30)

    stats = analyze_tail_digits()
    for tail, count in stats:
        print(f"尾數 {tail}：{count} 次")
