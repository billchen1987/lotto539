# 📦 匯入模組
import os
import sys
from pathlib import Path
import subprocess

# 📁 全域設定
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lotto539.db"
CSV_DIR = BASE_DIR / "data"

# 📋 功能選單
def main_menu():
    print("\n🎯 今彩539 分析系統 主選單")
    print("=" * 30)
    print("1. 下載最新 CSV 資料")
    print("2. 匯入 CSV 到資料庫")
    print("3. 執行統計摘要分析")
    print("4. 產出圖表")
    print("5. 產出 PDF 報告")
    print("6. 啟動 Web 介面（Streamlit）")
    print("7. 產出每週號碼統計 PDF 報表")  # ← 在選單中加入
    print("0. 離開")
    print("=" * 30)

    choice = input("請輸入選項：").strip()
    return choice

# ✅ 執行各子腳本
def run_script(script_name):
    script_path = BASE_DIR / script_name
    if not script_path.exists():
        print(f"❌ 找不到腳本：{script_name}")
        return
    subprocess.run([sys.executable, str(script_path)])

# 🚀 主流程
if __name__ == "__main__":
    while True:
        choice = main_menu()

        if choice == "1":
            run_script("fetch_csv.py")
        elif choice == "2":
            run_script("import_csv.py")
        elif choice == "3":
            run_script("summary.py")
        elif choice == "4":
            run_script("chart_generator.py")
        elif choice == "5":
            run_script("pdf_template.py")
        elif choice == "6":
            print("🔄 啟動 Streamlit Web 應用...")
            subprocess.run(["streamlit", "run", "streamlit_app.py"])
        elif choice == "7":
            run_script("report/weekly_number_report.py")
        elif choice == "0":
            print("👋 感謝使用，再見！")
            break
        else:
            print("⚠️ 無效選項，請重新輸入")
