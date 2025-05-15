# 📦 匯入模組
import sqlite3
from collections import Counter
from pathlib import Path
from datetime import datetime

# 📁 全域變數
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lotto539.db"

# ⏱️ 日期格式轉換（共用）
def normalize_date(input_str):
    for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%Y.%m.%d"):
        try:
            return datetime.strptime(input_str.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"❌ 無法解析日期格式：{input_str}")

# 📊 查詢各星期的開獎次數
def get_weekday_statistics(start_date=None, end_date=None):
    query = "SELECT weekday FROM lotto539"
    params = ()

    if start_date and end_date:
        start_fmt = normalize_date(start_date)
        end_fmt = normalize_date(end_date)
        query += " WHERE draw_date BETWEEN ? AND ?"
        params = (start_fmt, end_fmt)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

    weekdays = [row[0] for row in rows]
    counter = Counter(weekdays)
    return dict(sorted(counter.items(), key=lambda x: ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"].index(x[0])))

# 🚀 主程式
if __name__ == "__main__":
    print("📅 輸入日期區間（留空表示統計全部）：")
    start = input("➡️ 起始日期（如 2023/01/01）：").strip()
    end = input("➡️ 結束日期（如 2023/12/31）：").strip()

    try:
        stats = get_weekday_statistics(start if start else None, end if end else None)
        print("\n📊 各星期開獎次數統計：")
        for day, count in stats.items():
            print(f"{day}：{count} 次")
    except ValueError as e:
        print(e)
