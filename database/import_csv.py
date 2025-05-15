# 📦 匯入模組
import sqlite3
import csv
from pathlib import Path
from datetime import datetime

# 📁 全域變數
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "lotto539.db"
DATA_DIR = BASE_DIR / "data"
LATEST_PATH_FILE = DATA_DIR / ".latest_csv_path"

# 🔍 從 latest_csv_path 取得最新 CSV 路徑
if not LATEST_PATH_FILE.exists():
    print("[ERROR] 找不到 .latest_csv_path 檔案")
    exit()

with open(LATEST_PATH_FILE, "r", encoding="utf-8") as f:
    latest_csv = Path(f.read().strip())

if not latest_csv.exists():
    print(f"[ERROR] 指定的 CSV 檔案不存在：{latest_csv}")
    exit()

print(f"[INFO] 讀取 CSV 檔案：{latest_csv}")

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    inserted, skipped = 0, 0

    with open(latest_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)  # 跳過標題列

        for row in reader:
            try:
                draw_date = datetime.strptime(row[0].strip(), "%Y/%m/%d").strftime("%Y-%m-%d")
                period = row[1].strip()
                numbers = [int(row[i]) for i in range(2, 7)]
                weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][datetime.strptime(draw_date, "%Y-%m-%d").weekday()]

                cursor.execute("""
                    INSERT OR IGNORE INTO lotto539
                    (period, draw_date, weekday, no1, no2, no3, no4, no5)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (period, draw_date, weekday, *numbers))

                if cursor.rowcount:
                    inserted += 1
                else:
                    skipped += 1

            except Exception as e:
                print(f"[WARN] 匯入失敗（期別 {row[1]}）：{e}")

    conn.commit()
    print(f"[INFO] 匯入完成：新增 {inserted} 筆，跳過 {skipped} 筆（已存在）")
