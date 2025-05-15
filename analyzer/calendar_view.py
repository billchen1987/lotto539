import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def get_full_date_range(data):
    df = pd.DataFrame(data, columns=["期別", "開獎日期", "星期", "號碼1", "號碼2", "號碼3", "號碼4", "號碼5"])
    df["開獎日期"] = pd.to_datetime(df["開獎日期"])
    return df["開獎日期"].min().date(), df["開獎日期"].max().date()

def show_calendar_style_table(data):
    st.subheader("\U0001F4CB 月曆式開獎紀錄（A3 格式模擬）")

    with st.expander("\U0001F50D 開獎號碼查詢條件（最多輸入 5 組）"):
        col_query = st.columns(5)
        query_colors = ["#fca5a5", "#fdba74", "#fcd34d", "#86efac", "#93c5fd"]
        query_values = []
        for i in range(5):
            val = col_query[i].text_input(f"查詢號碼 {i+1}", key=f"query_{i}").strip()
            if val and (not val.isdigit() or not (1 <= int(val) <= 39)):
                st.warning(f"⚠️ 查詢號碼 {i+1} 僅能輸入 1~39 的整數")
            query_values.append(val)
        query_colors = [col_query[i].color_picker("選擇顏色", query_colors[i], key=f"color_{i}") for i in range(5)]

    full_start, full_end = get_full_date_range(data)
    today = datetime.today().date()
    default_end = min(today, full_end)
    df_all = pd.DataFrame(data, columns=["期別", "開獎日期", "星期", "號碼1", "號碼2", "號碼3", "號碼4", "號碼5"])
    df_all["開獎日期"] = pd.to_datetime(df_all["開獎日期"])
    df_range = df_all[df_all["開獎日期"] <= pd.to_datetime(default_end)].sort_values(by="開獎日期", ascending=False).head(144)
    default_start = df_range["開獎日期"].min().date()

    col1, col2 = st.columns(2)
    user_start = col1.date_input("起始日期", value=default_start, min_value=full_start, max_value=default_end)
    user_end = col2.date_input("結束日期", value=default_end, min_value=full_start, max_value=default_end)

    if user_start > user_end:
        st.warning("⚠️ 起始日不能大於結束日")
        return

    df = pd.DataFrame(data, columns=["期別", "開獎日期", "星期", "號碼1", "號碼2", "號碼3", "號碼4", "號碼5"])
    df["開獎日期"] = pd.to_datetime(df["開獎日期"])
    df = df[(df["開獎日期"] >= pd.to_datetime(user_start)) & (df["開獎日期"] <= pd.to_datetime(user_end))].copy()
    df = df.sort_values(by="開獎日期", ascending=False).head(144).sort_values(by="開獎日期").reset_index(drop=True)
    user_start = df["開獎日期"].min().date()
    user_end = df["開獎日期"].max().date()
    df = df.sort_values(by="開獎日期").reset_index(drop=True)

    df[["號碼1", "號碼2", "號碼3", "號碼4", "號碼5"]] = df[["號碼1", "號碼2", "號碼3", "號碼4", "號碼5"]].apply(pd.to_numeric, errors='coerce')
    df[["號碼1", "號碼2", "號碼3", "號碼4", "號碼5"]] = df[["號碼1", "號碼2", "號碼3", "號碼4", "號碼5"]].apply(lambda row: sorted(row), axis=1, result_type='expand')
    df["月"] = df["開獎日期"].dt.strftime("%m")
    df["日"] = df["開獎日期"].dt.strftime("%d")
    df = df[["月", "日", "星期", "號碼1", "號碼2", "號碼3", "號碼4", "號碼5"]].reset_index(drop=True)
    df = df.head(144)

    while len(df) < 144:
        df.loc[len(df)] = ["" for _ in range(df.shape[1])]
    df = df.iloc[:144]

    table_rows = []
    for row_index in range(36):
        row_data = []
        for col_group in range(4):
            base_idx = row_index + 36 * col_group
            row = df.iloc[base_idx]
            group = [
                row["月"], row["日"], row["星期"],
                row["號碼1"], row["號碼2"], row["號碼3"], row["號碼4"], row["號碼5"]
            ]
            row_data.extend(group)
        table_rows.append(row_data)

    col_names = []
    for i in range(1, 5):
        col_names.extend([
            f"月{i}", f"日{i}", f"星期{i}",
            f"號碼1_{i}", f"號碼2_{i}", f"號碼3_{i}", f"號碼4_{i}", f"號碼5_{i}"
        ])

    final_table = pd.DataFrame(table_rows, columns=col_names).astype(str)
    final_table = final_table.applymap(lambda v: v.zfill(2) if v.isdigit() else v)

    highlight_style = pd.DataFrame("", index=final_table.index, columns=final_table.columns)
    used_values = set()
    for qval_raw, color in zip(query_values, query_colors):
        if not qval_raw.strip():
            continue

        qval = qval_raw.strip().zfill(2)

        if not qval.isdigit() or not (1 <= int(qval) <= 39):
            st.warning(f"⚠️ 查詢號碼 {qval_raw} 僅能輸入 1~39 的整數")
            continue

        if qval in used_values:
            st.warning(f"⚠️ 查詢號碼 {qval} 輸入重複，請移除重複值")
            continue

        used_values.add(qval)

        for col in final_table.columns:
            if not col.startswith(("月", "日", "星期")):
                highlight_style.loc[final_table[col] == qval, col] = f"background-color: {color}"

    styled = final_table.style.apply(
        lambda df: pd.DataFrame(
            [[
                highlight_style.loc[df.index[row_idx], c] if highlight_style.loc[df.index[row_idx], c] else (
                    "background-color: #fef3c7" if c.startswith(("月1", "日1", "星期1")) else
                    "background-color: #e0f2fe" if c.startswith(("月2", "日2", "星期2")) else
                    "background-color: #ede9fe" if c.startswith(("月3", "日3", "星期3")) else
                    "background-color: #dcfce7" if c.startswith(("月4", "日4", "星期4")) else
                    ""
                ) for c in df.columns
            ] for row_idx in range(len(df))],
            columns=df.columns
        ),
        axis=None
    ).set_properties(**{
        'text-align': 'center',
        'border': '1px solid black',
        'font-size': '9pt'
    })

    st.markdown(f"### 今彩539（起始日：{user_start.strftime('%Y/%m/%d')}，結束日：{user_end.strftime('%Y/%m/%d')}）")
    st.dataframe(styled, use_container_width=True, height=1600)
