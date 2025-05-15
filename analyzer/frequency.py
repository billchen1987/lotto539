# 📦 匯入模組
import sqlite3
from collections import Counter
from pathlib import Path

# 📁 路徑設定
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lotto539.db"

# 📊 號碼出現頻率統計
def get_number_frequency(limit=None, ascending=False):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        numbers = [n for row in cursor.fetchall() for n in row]

    counter = Counter(numbers)
    sorted_freq = sorted(counter.items(), key=lambda x: x[1], reverse=not ascending)

    if limit:
        return sorted_freq[:limit]
    return sorted_freq

# 🚀 主程式
if __name__ == "__main__":
    print("📈 今彩539 號碼出現頻率分析")
    print("=" * 35)

    try:
        limit = input("➡️ 顯示前幾名？（空白表示全部）：").strip()
        order = input("🔼 顯示順序？輸入 asc 為冷門、留空為熱門：").strip().lower()

        limit = int(limit) if limit else None
        ascending = True if order == "asc" else False

        freq_list = get_number_frequency(limit=limit, ascending=ascending)

        print("\n📊 號碼頻率結果：")
        for num, count in freq_list:
            print(f"號碼 {num:2d} 出現 {count} 次")
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
