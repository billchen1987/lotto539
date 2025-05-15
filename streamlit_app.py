# 📦 匯入模組
import sys
import time
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from collections import Counter
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
from analyzer.gap_analysis import analyze_single_number, plot_gap_trend
from analyzer.calendar_view import show_calendar_style_table


# ✅ 中文字型設定
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 📁 全域設定
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lotto539.db"
REPORTS_DIR = BASE_DIR / "reports"

# 🚀 資料載入函式
@st.cache_data
def load_lotto_data():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT period, draw_date, weekday, no1, no2, no3, no4, no5 FROM lotto539 ORDER BY draw_date DESC")
        return cursor.fetchall()

# 📈 各分析區塊模組

def show_hot_number_chart(data):
    st.subheader("🔥 熱門號碼前 10 名")
    numbers = [n for row in data for n in row[3:]]
    top10 = Counter(numbers).most_common(10)
    labels, values = zip(*top10)
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title("熱門號碼出現次數")
    st.pyplot(fig)

def show_tail_digit_chart(data):
    st.subheader("🔢 尾數出現次數")
    numbers = [n for row in data for n in row[3:]]
    tails = [n % 10 for n in numbers]
    counter = Counter(tails)
    labels, values = zip(*sorted(counter.items()))
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title("尾數分布")
    st.pyplot(fig)

def show_odd_even_pie(data):
    st.subheader("⚖ 奇偶比例")
    numbers = [n for row in data for n in row[3:]]
    odd = sum(1 for n in numbers if n % 2 == 1)
    even = sum(1 for n in numbers if n % 2 == 0)
    fig, ax = plt.subplots()
    ax.pie([odd, even], labels=["奇數", "偶數"], autopct="%1.1f%%", startangle=90)
    ax.set_title("奇偶數比例")
    st.pyplot(fig)

def show_summary_section(data):
    st.subheader("📈 總體統計資訊")
    first_date, last_date = data[-1][1], data[0][1]
    st.write(f"🗓 資料期間：**{first_date} ~ {last_date}**")
    st.write(f"📊 總期數：**{len(data)} 期**")

    numbers = [n for row in data for n in row[3:]]
    counter = Counter(numbers)
    top5 = counter.most_common(5)
    bottom5 = counter.most_common()[-5:]
    st.write("🔥 熱門號碼（前 5）：", ', '.join(f"{n} ({c} 次)" for n, c in top5))
    st.write("❄️ 冷門號碼（後 5）：", ', '.join(f"{n} ({c} 次)" for n, c in bottom5))

    odd = sum(1 for n in numbers if n % 2 == 1)
    even = sum(1 for n in numbers if n % 2 == 0)
    st.write(f"⚖️ 奇偶比：**{odd}:{even}**")

# 📅 各星期號碼出現統計

def show_weekday_chart(data):
    st.subheader("📅 各星期號碼出現次數與比例")
    weekday_map = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    number_range = list(range(1, 40))
    stats = {day: Counter() for day in weekday_map}

    for row in data:
        weekday = row[2]
        numbers = row[3:]
        for n in numbers:
            stats[weekday][n] += 1

    percentage_stats = {}
    for day in weekday_map:
        total = sum(stats[day].values())
        percentage_stats[day] = {
            n: f"{(stats[day][n] / total * 100):.2f}%" if total > 0 else "0.00%"
            for n in number_range
        }

    # 組成表格資料
    table_data = []
    for day in weekday_map:
        row = [day] + [f"{stats[day][n]} ({percentage_stats[day][n]})" for n in number_range]
        table_data.append(row)

    df = pd.DataFrame(table_data, columns=["星期"] + [f"{n:02d}" for n in number_range])
    st.dataframe(df, use_container_width=True)

    # 顯示熱力圖（轉置：星期為欄）
    st.subheader("🌡️ 出現次數熱力圖")
    heatmap_data = pd.DataFrame({day: [stats[day][n] for n in number_range] for day in weekday_map}, index=[f"{n:02d}" for n in number_range])
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", cbar=True, linewidths=.5, linecolor='gray', ax=ax)
    ax.set_title("號碼 vs 星期出現熱力圖")
    st.pyplot(fig)

def show_latest_records(data):
    st.subheader("📄 最新開獎資料（前 10 筆）")
    df = pd.DataFrame(data[:10], columns=["期別", "開獎日期", "星期", "號碼1", "號碼2", "號碼3", "號碼4", "號碼5"])
    st.dataframe(df)

def show_pdf_download():
    st.subheader("📥 報表下載")
    today = datetime.now().strftime("%Y%m%d")
    report_path = REPORTS_DIR / f"weekly_number_summary_{today}.pdf"

    if "report_ready" not in st.session_state:
        st.session_state.report_ready = report_path.exists()

    if not st.session_state.report_ready:
        if st.button("📄 立即產出報表"):
            with st.spinner("正在產出 PDF 報表，請稍候..."):
                subprocess.run([sys.executable, str(BASE_DIR / "report" / "weekly_number_report.py")])
                time.sleep(3)
                if report_path.exists():
                    st.session_state.report_ready = True
                    st.rerun()

    if st.session_state.report_ready and report_path.exists():
        with open(report_path, "rb") as f:
            st.download_button("📥 下載每週統計報表 (PDF)", f, file_name=report_path.name)

# 🚀 主介面
st.set_page_config(page_title="今彩539 數據分析", layout="wide")
st.title("🎯 今彩539 數據分析平台")

try:
    data = load_lotto_data()
    if len(data) == 0:
        st.warning("⚠️ 資料庫中尚無資料，請先匯入歷史開獎紀錄。")
        st.stop()

    tab = st.sidebar.radio("📂 選擇分析項目", (
        "總體統計",
        "熱門號碼分析",
        "尾數出現分布",
        "奇偶比例",
        "星期分布",
        "最新期別資料",
        "號碼間隔分析",
        "月曆式開獎紀錄",
        "報表下載"
    ))

    

    if tab == "總體統計":
        show_summary_section(data)
    elif tab == "熱門號碼分析":
        show_hot_number_chart(data)
    elif tab == "尾數出現分布":
        show_tail_digit_chart(data)
    elif tab == "奇偶比例":
        show_odd_even_pie(data)
    elif tab == "星期分布":
        show_weekday_chart(data)
    elif tab == "最新期別資料":
        show_latest_records(data)
    elif tab == "號碼間隔分析":
        st.subheader("🔍 號碼間隔與冷熱分析")
        number_input = st.text_input("請輸入要分析的號碼（01~39）", "01")
        if number_input.strip().isdigit() and 1 <= int(number_input) <= 39:
            result = analyze_single_number(number_input)
            st.write(f"➡️ 當前間隔期數：**{result['current_gap']}** 期")

            if result['stats']:
                st.write("📊 歷史間隔統計：")
                stats = result['stats']
                st.markdown(f"- 最大間隔：{stats['max']} 期")
                st.markdown(f"- 最小間隔：{stats['min']} 期")
                st.markdown(f"- 平均間隔：{stats['avg']} 期")
                st.markdown(f"- 中位數：{stats['median']} 期")
                st.write(f"📌 狀態評估：**{result['state']}**")

                chart_path = plot_gap_trend(result['history'], int(number_input))
                st.image(str(chart_path), caption=f"號碼 {number_input} 間隔趨勢圖", use_container_width=True)

            else:
                st.info("⚠️ 無足夠歷史資料可分析")
        else:
            st.warning("請輸入 01 至 39 的有效號碼")
    elif tab == "月曆式開獎紀錄":
        show_calendar_style_table(data)
    elif tab == "報表下載":
        show_pdf_download()

except Exception as e:
    st.error(f"❌ 發生錯誤：{e}")
