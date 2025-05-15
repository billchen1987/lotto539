# 📦 匯入模組
import sqlite3
from pathlib import Path

# 📁 全域設定
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lotto539.db"

# 🔗 分析連號分布
def analyze_consecutive_numbers():
    total_consecutive_periods = 0
    consecutive_count_distribution = {}

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT period, no1, no2, no3, no4, no5 FROM lotto539")
        rows = cursor.fetchall()

    for row in rows:
        period = row[0]
        numbers = sorted(row[1:])
        count = 0

        for i in range(4):
            if numbers[i] + 1 == numbers[i + 1]:
                count += 1

        if count > 0:
            total_consecutive_periods += 1

        # 累積出現次數分類
        consecutive_count_distribution[count] = consecutive_count_distribution.get(count, 0) + 1

    return total_consecutive_periods, consecutive_count_distribution

# 🚀 主程式
if __name__ == "__main__":
    print("🔗 今彩539 連號分析")
    print("=" * 30)

    total, distribution = analyze_consecutive_numbers()

    print(f"📈 出現連號的期數：{total} 期")
    print("\n📊 每期中連號數量的分布情形：")
    for count in sorted(distribution):
        print(f"  含 {count} 組連號：{distribution[count]} 期")
