# 📦 匯入套件
import sqlite3
import os
from pathlib import Path

# 📁 全域變數設定
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "lotto539.db"

# 🧱 建立資料表的 SQL 指令
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS lotto539 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period TEXT UNIQUE NOT NULL,
    draw_date TEXT NOT NULL,
    weekday TEXT NOT NULL,
    no1 INTEGER NOT NULL,
    no2 INTEGER NOT NULL,
    no3 INTEGER NOT NULL,
    no4 INTEGER NOT NULL,
    no5 INTEGER NOT NULL,
    remark TEXT DEFAULT ''
);
"""

# 🔧 初始化資料庫函式
def initialize_database():
    try:
        if DB_PATH.exists():
            print(f"✔️ 資料庫已存在：{DB_PATH}")
        else:
            print(f"📂 建立資料庫：{DB_PATH}")
        
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_TABLE_SQL)
            conn.commit()
            print("✅ 資料表建立完成（或已存在）")
    except sqlite3.Error as e:
        print(f"❌ 資料庫初始化失敗：{e}")

# 🚀 主程式入口點
if __name__ == "__main__":
    initialize_database()
