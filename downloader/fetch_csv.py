import requests
from pathlib import Path
from datetime import datetime

# 📁 全域設定
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILENAME = f"lotto539_{datetime.now().strftime('%Y%m%d')}.csv"
CSV_PATH = DATA_DIR / CSV_FILENAME
LATEST_PATH_FILE = DATA_DIR / ".latest_csv_path"

# 🔗 資料來源 URL（可更換為實際來源）
CSV_URL = "https://biga.com.tw/HISTORYDATA/tw539.csv"

# 📥 下載函式
def fetch_lotto_csv():
    try:
        print(f"[INFO] 資料儲存目錄：{DATA_DIR}")
        response = requests.get(CSV_URL, timeout=10)
        response.raise_for_status()

        with open(CSV_PATH, "wb") as f:
            f.write(response.content)

        print(f"[INFO] 檔案已儲存：{CSV_PATH}")

        # 寫入最新 CSV 路徑至暫存檔
        with open(LATEST_PATH_FILE, "w", encoding="utf-8") as f:
            f.write(str(CSV_PATH))

        return CSV_PATH

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 下載失敗：{e}")
        return None

# 🚀 主程式入口
if __name__ == "__main__":
    fetch_lotto_csv()
