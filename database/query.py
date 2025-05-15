# 📦 匯入模組
import sqlite3
from collections import Counter
from pathlib import Path
from datetime import datetime

# 📁 全域設定
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lotto539.db"

# ⏱️ 輔助函式：標準化使用者輸入的日期格式
def normalize_date(input_str):
    for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%Y.%m.%d", "%Y/%-m/%-d", "%Y-%m-%d"):
        try:
            return datetime.strptime(input_str.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"❌ 日期格式無法解析：{input_str}")

# 🔍 取得所有號碼資料
def fetch_all_numbers():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        return [num for row in cursor.fetchall() for num in row]

# 🔢 熱號查詢（出現次數排序）
def query_hot_numbers():
    numbers = fetch_all_numbers()
    counter = Counter(numbers)
    return counter.most_common()

# 🧠 尾數統計
def query_tail_numbers():
    numbers = fetch_all_numbers()
    tail_counter = Counter([n % 10 for n in numbers])
    return sorted(tail_counter.items())

# ⚖️ 奇偶比
def query_odd_even_ratio():
    numbers = fetch_all_numbers()
    odd = sum(1 for n in numbers if n % 2 == 1)
    even = sum(1 for n in numbers if n % 2 == 0)
    return {"奇數": odd, "偶數": even}

# 🔗 連號出現次數
def query_consecutive_count():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        consecutive_total = 0
        for row in cursor.fetchall():
            sorted_nums = sorted(row)
            for i in range(4):
                if sorted_nums[i] + 1 == sorted_nums[i + 1]:
                    consecutive_total += 1
        return consecutive_total

# 📅 區間查詢統計（含星期統計）
def query_by_date_range(start_date: str, end_date: str):
    try:
        start_date_fmt = normalize_date(start_date)
        end_date_fmt = normalize_date(end_date)
    except ValueError as e:
        print(e)
        return []

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT period, draw_date, weekday, no1, no2, no3, no4, no5
            FROM lotto539
            WHERE draw_date BETWEEN ? AND ?
            ORDER BY draw_date
        """, (start_date_fmt, end_date_fmt))
        return cursor.fetchall()

# 🚀 主程式範例執行（可依功能選用）
if __name__ == "__main__":
    print("📊 熱門號碼：")
    for num, count in query_hot_numbers():
        print(f"號碼 {num:2d} 出現 {count} 次")

    print("\n🧪 尾數統計：")
    for tail, count in query_tail_numbers():
        print(f"尾數 {tail}：{count} 次")

    print("\n⚖️ 奇偶統計：")
    print(query_odd_even_ratio())

    print("\n🔗 連號總次數：")
    print(query_consecutive_count())

    print("\n📅 2024年查詢結果（部分）：")
    results = query_by_date_range("2024/01/01", "2024/12/31")
    for row in results[:3]:
        print(row)
