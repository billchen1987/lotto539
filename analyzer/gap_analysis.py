# 📦 匯入模組
import sqlite3
from pathlib import Path
from collections import defaultdict
import statistics
import matplotlib.pyplot as plt

# 📁 路徑設定
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "lotto539.db"

# 🔍 分析單一號碼的間隔資料
def analyze_single_number(target_number):
    target_number = int(target_number)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT draw_date, no1, no2, no3, no4, no5 FROM lotto539 ORDER BY draw_date DESC")
        rows = cursor.fetchall()

    gap_list = []
    last_seen_index = None

    for index, row in enumerate(rows):
        date, *numbers = row
        if target_number in numbers:
            if last_seen_index is not None:
                gap_list.append(index - last_seen_index)  # ✅ 修正方向，間隔期數應為遞增距離
            last_seen_index = index

    current_gap = last_seen_index if last_seen_index is not None else len(rows)

    if not gap_list:
        return {
            "current_gap": current_gap,
            "history": [],
            "stats": None,
            "state": "首度分析，無歷史資料",
        }

    # 統計分析
    max_gap = max(gap_list)
    min_gap = min(gap_list)
    avg_gap = round(sum(gap_list) / len(gap_list), 2)
    median_gap = statistics.median(gap_list)
    state = "🔥 熱號" if current_gap <= avg_gap else "❄️ 冷號"

    return {
        "current_gap": current_gap,
        "history": gap_list,
        "stats": {
            "max": max_gap,
            "min": min_gap,
            "avg": avg_gap,
            "median": median_gap
        },
        "state": state
    }

# 📊 繪製號碼間隔趨勢圖
def plot_gap_trend(gap_list, target_number):
    plt.figure(figsize=(10, 4))
    plt.plot(range(1, len(gap_list) + 1), gap_list, marker='o', linestyle='-')
    plt.title(f"號碼 {target_number:02d} 的歷史間隔趨勢")
    plt.xlabel("出現次數（由近到遠）")
    plt.ylabel("間隔期數")
    plt.grid(True)
    plt.tight_layout()
    chart_path = BASE_DIR / f"charts/gap_{target_number:02d}.png"
    chart_path.parent.mkdir(exist_ok=True)
    plt.savefig(chart_path)
    plt.close()
    return chart_path

# 🧪 測試執行
if __name__ == "__main__":
    number = input("輸入要分析的號碼（01~39）：").zfill(2)
    result = analyze_single_number(number)
    print(f"\n🎯 號碼 {number} 分析結果")
    print(f"➡️ 當前間隔期數：{result['current_gap']} 期")

    if result['stats']:
        print("📊 歷史間隔統計：")
        for k, v in result['stats'].items():
            print(f"   {k}：{v}")
        print(f"📌 狀態評估：{result['state']}")

        path = plot_gap_trend(result['history'], int(number))
        print(f"📈 圖表已儲存：{path}")
    else:
        print("⚠️ 無足夠歷史資料可分析")
# 📦 匯入模組
import sqlite3
from pathlib import Path
from collections import defaultdict
import statistics
import matplotlib.pyplot as plt

# 📁 路徑設定
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "lotto539.db"

# 🔍 分析單一號碼的間隔資料
def analyze_single_number(target_number):
    target_number = int(target_number)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT draw_date, no1, no2, no3, no4, no5 FROM lotto539 ORDER BY draw_date DESC")
        rows = cursor.fetchall()

    gap_list = []
    last_seen_index = None

    for index, row in enumerate(rows):
        date, *numbers = row
        if target_number in numbers:
            if last_seen_index is not None:
                gap_list.append(index - last_seen_index)  # ✅ 修正方向，間隔期數應為遞增距離
            last_seen_index = index

    current_gap = last_seen_index if last_seen_index is not None else len(rows)

    if not gap_list:
        return {
            "current_gap": current_gap,
            "history": [],
            "stats": None,
            "state": "首度分析，無歷史資料",
        }

    # 統計分析
    max_gap = max(gap_list)
    min_gap = min(gap_list)
    avg_gap = round(sum(gap_list) / len(gap_list), 2)
    median_gap = statistics.median(gap_list)
    state = "🔥 熱號" if current_gap <= avg_gap else "❄️ 冷號"

    return {
        "current_gap": current_gap,
        "history": gap_list,
        "stats": {
            "max": max_gap,
            "min": min_gap,
            "avg": avg_gap,
            "median": median_gap
        },
        "state": state
    }

# 📊 繪製號碼間隔趨勢圖
def plot_gap_trend(gap_list, target_number):
    plt.figure(figsize=(10, 4))
    plt.plot(range(1, len(gap_list) + 1), gap_list, marker='o', linestyle='-')
    plt.title(f"號碼 {target_number:02d} 的歷史間隔趨勢")
    plt.xlabel("出現次數（由近到遠）")
    plt.ylabel("間隔期數")
    plt.grid(True)
    plt.tight_layout()
    chart_path = BASE_DIR / f"charts/gap_{target_number:02d}.png"
    chart_path.parent.mkdir(exist_ok=True)
    plt.savefig(chart_path)
    plt.close()
    return chart_path

# 🧪 測試執行
if __name__ == "__main__":
    number = input("輸入要分析的號碼（01~39）：").zfill(2)
    result = analyze_single_number(number)
    print(f"\n🎯 號碼 {number} 分析結果")
    print(f"➡️ 當前間隔期數：{result['current_gap']} 期")

    if result['stats']:
        print("📊 歷史間隔統計：")
        for k, v in result['stats'].items():
            print(f"   {k}：{v}")
        print(f"📌 狀態評估：{result['state']}")

        path = plot_gap_trend(result['history'], int(number))
        print(f"📈 圖表已儲存：{path}")
    else:
        print("⚠️ 無足夠歷史資料可分析")
