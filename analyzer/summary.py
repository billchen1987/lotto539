# 📦 匯入模組
import sqlite3
from collections import Counter
from pathlib import Path
from datetime import datetime

# 📁 全域路徑
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lotto539.db"

# 🧠 分析資料摘要
def summarize_statistics():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # 總筆數與日期範圍
        cursor.execute("SELECT COUNT(*), MIN(draw_date), MAX(draw_date) FROM lotto539")
        total_rows, start_date, end_date = cursor.fetchone()

        # 所有號碼平攤為一個 list
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        all_numbers = [num for row in cursor.fetchall() for num in row]
        number_counter = Counter(all_numbers)

        # 奇偶比例
        odd = sum(1 for n in all_numbers if n % 2 == 1)
        even = sum(1 for n in all_numbers if n % 2 == 0)

        # 尾數分析
        tail_counter = Counter(n % 10 for n in all_numbers)

        # 連號次數
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        consecutive_count = 0
        for row in cursor.fetchall():
            sorted_row = sorted(row)
            for i in range(4):
                if sorted_row[i] + 1 == sorted_row[i + 1]:
                    consecutive_count += 1

        # 星期統計
        cursor.execute("SELECT weekday FROM lotto539")
        weekdays = [row[0] for row in cursor.fetchall()]
        weekday_counter = Counter(weekdays)

    # 🧾 顯示結果
    print("📊 今彩539 數據摘要分析")
    print("=" * 40)
    print(f"📆 資料期間：{start_date} ～ {end_date}")
    print(f"🧾 總期數：{total_rows} 期")
    print(f"🔢 熱門號碼（前5）：{number_counter.most_common(5)}")
    print(f"❄️ 冷門號碼（後5）：{number_counter.most_common()[-5:]}")
    print(f"🧠 常見尾數（前3）：{tail_counter.most_common(3)}")
    print(f"⚖️ 奇數：{odd}，偶數：{even}（奇偶比 {odd}:{even}）")
    print(f"🔗 出現連號期數總計：{consecutive_count} 次")
    print("📅 各星期開獎次數：")
    for day in ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]:
        print(f"  {day}：{weekday_counter.get(day, 0)} 次")
    print("=" * 40)

# 🚀 主程式
if __name__ == "__main__":
    summarize_statistics()
