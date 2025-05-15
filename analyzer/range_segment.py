# 📦 匯入模組
import sqlite3
from pathlib import Path
from collections import Counter

# 📁 全域變數
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lotto539.db"

# 🔢 區間標籤
SEGMENT_LABELS = {
    1: "01-10",
    2: "11-20",
    3: "21-30",
    4: "31-39"
}

# 🧠 計算每個號碼所屬區段
def get_segment(num):
    if 1 <= num <= 10:
        return 1
    elif 11 <= num <= 20:
        return 2
    elif 21 <= num <= 30:
        return 3
    elif 31 <= num <= 39:
        return 4
    else:
        return 0  # 非法號碼

# 📊 區間分析主函式
def analyze_range_segments():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT no1, no2, no3, no4, no5 FROM lotto539")
        rows = cursor.fetchall()

    segment_counter = Counter()

    for row in rows:
        for num in row:
            segment = get_segment(num)
            if segment:
                segment_counter[segment] += 1

    # 依照 1~4 區段排序並轉成標籤輸出
    return {SEGMENT_LABELS[k]: segment_counter[k] for k in sorted(SEGMENT_LABELS)}

# 🚀 主程式
if __name__ == "__main__":
    print("📊 今彩539 數值區間分析（每顆號碼）")
    print("=" * 40)

    results = analyze_range_segments()
    total = sum(results.values())

    for label, count in results.items():
        ratio = round((count / total) * 100, 2)
        print(f"區間 {label}：{count} 次（{ratio}%）")
