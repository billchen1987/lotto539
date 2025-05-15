# 📦 匯入模組
import sqlite3
from collections import Counter
from pathlib import Path

# 📁 全域變數
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lotto539.db"

# 🔥 取得熱號與冷號
def get_hot_and_cold_numbers(top_n=5):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        all_numbers = [n for row in cursor.fetchall() for n in row]

    counter = Counter(all_numbers)
    most_common = counter.most_common()

    hot = most_common[:top_n]
    cold = most_common[-top_n:]
    return hot, cold

# 🚀 主程式
if __name__ == "__main__":
    try:
        print("🔥 今彩539 熱號 / 冷號 分析")
        print("=" * 32)
        n = input("➡️ 要顯示前幾名？（預設5）：").strip()
        top_n = int(n) if n else 5

        hot, cold = get_hot_and_cold_numbers(top_n=top_n)

        print(f"\n🔥 熱門前 {top_n} 號碼：")
        for num, count in hot:
            print(f"號碼 {num:2d} ➜ {count} 次")

        print(f"\n❄️ 冷門後 {top_n} 號碼：")
        for num, count in cold:
            print(f"號碼 {num:2d} ➜ {count} 次")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
