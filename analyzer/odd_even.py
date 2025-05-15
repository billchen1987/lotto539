# 📦 匯入模組
import sqlite3
from pathlib import Path

# 📁 全域設定
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lotto539.db"

# ⚖️ 奇偶統計分析
def analyze_odd_even():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        numbers = [n for row in cursor.fetchall() for n in row]

    odd_count = sum(1 for n in numbers if n % 2 == 1)
    even_count = sum(1 for n in numbers if n % 2 == 0)
    total = len(numbers)

    odd_ratio = round((odd_count / total) * 100, 2)
    even_ratio = round((even_count / total) * 100, 2)

    return {
        "奇數": odd_count,
        "偶數": even_count,
        "奇數比例": f"{odd_ratio}%",
        "偶數比例": f"{even_ratio}%"
    }

# 🚀 主程式
if __name__ == "__main__":
    print("⚖️ 今彩539 奇偶數分析")
    print("=" * 30)

    result = analyze_odd_even()
    print(f"🔢 奇數總數：{result['奇數']} 次")
    print(f"🔢 偶數總數：{result['偶數']} 次")
    print(f"📊 奇數比例：{result['奇數比例']}")
    print(f"📊 偶數比例：{result['偶數比例']}")
