# 📦 匯入模組
import sqlite3
from collections import defaultdict
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ✅ 註冊中文字型
pdfmetrics.registerFont(TTFont("JhengHei", "msjh.ttc"))

# 📁 全域路徑
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "lotto539.db"
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)
PDF_PATH = REPORT_DIR / f"weekly_number_summary_{datetime.now().strftime('%Y%m%d')}.pdf"

# 📅 對應星期中文
WEEKDAY_MAP = {
    "星期一": "一",
    "星期二": "二",
    "星期三": "三",
    "星期四": "四",
    "星期五": "五",
    "星期六": "六",
    "星期日": "日"
}

ALL_NUMBERS = [f"{i:02d}" for i in range(1, 40)]
SECTION_COLORS = {
    "一": colors.Color(0.85, 0.88, 0.95),
    "二": colors.Color(0.85, 0.88, 0.95),
    "三": colors.Color(0.88, 0.95, 0.85),
    "四": colors.Color(0.88, 0.95, 0.85),
    "五": colors.Color(0.9, 0.85, 0.95),
    "六": colors.Color(0.9, 0.85, 0.95),
    "日": colors.Color(0.9, 0.85, 0.95),
    "一、二加總": colors.Color(1, 1, 0.8),
    "三、四加總": colors.Color(1, 1, 0.8),
    "五、六、日加總": colors.Color(1, 1, 0.8),
    "一到日所有加總": colors.Color(1, 0.95, 0.8),
    "Count(驗證)": colors.Color(0.85, 0.92, 0.98)
}

# 📊 撈資料
def collect_weekday_number_counts():
    stats = {label: defaultdict(int) for label in WEEKDAY_MAP.values()}
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT weekday, no1, no2, no3, no4, no5, draw_date FROM lotto539 ORDER BY draw_date")
        rows = cursor.fetchall()
        for row in rows:
            wd = WEEKDAY_MAP.get(row[0], "")
            for num in row[1:6]:
                stats[wd][f"{num:02d}"] += 1
        last_date = rows[-1][-1] if rows else "N/A"
    return stats, last_date

# 🧮 建構報表資料
def build_report_rows(stats):
    def sum_rows(keys):
        combined = defaultdict(int)
        for key in keys:
            for k, v in stats[key].items():
                combined[k] += v
        return combined
    rows = [
        ("一", stats["一"]),
        ("二", stats["二"]),
        ("一、二加總", sum_rows(["一", "二"])),
        ("三", stats["三"]),
        ("四", stats["四"]),
        ("三、四加總", sum_rows(["三", "四"])),
        ("五", stats["五"]),
        ("六", stats["六"]),
        ("日", stats["日"]),
        ("五、六、日加總", sum_rows(["五", "六", "日"])),
    ]
    total = sum_rows(["一", "二", "三", "四", "五", "六", "日"])
    rows.append(("一到日所有加總", total))
    rows.append(("總計(驗證)", total))
    return rows

# 🖨️ 輸出 PDF
def generate_pdf(rows, last_date, debug=False):
    styles = getSampleStyleSheet()
    styles['Title'].fontName = 'JhengHei'
    styles.add(ParagraphStyle(name='SmallJhengHei', fontName='JhengHei', fontSize=7, leading=8, alignment=1))

    content = [Paragraph("539 號碼出現次數統計", styles['Title']), Spacer(1, 4)]
    content.append(Paragraph(f"<para alignment='left'>資料收集日期：{last_date}</para>", styles['SmallJhengHei']))
    content.append(Spacer(1, 6))

    header = ["星期"] + ALL_NUMBERS
    data = [header]

    for label, row_data in rows:
        if label == "五、六、日加總":
            wrapped_text = "五、六、<br/>日加總"
        elif "所有加總" in label:
            wrapped_text = label.upper() if label == "總計(驗證)" else label.replace("所有加總", "<br/>所有加總")
        elif "加總" in label:
            wrapped_text = label.replace("加總", "<br/>加總")
        elif "(驗證)" in label:
            wrapped_text = label.replace("(驗證)", "<br/>(驗證)")
        else:
            wrapped_text = label

        wrapped_label = Paragraph(wrapped_text, styles['SmallJhengHei'])
        row = [wrapped_label] + [str(row_data.get(n, 0)) for n in ALL_NUMBERS]
        data.append(row)

    label_max_width = max(len(Paragraph(label, styles['SmallJhengHei']).getPlainText()) for label, _ in rows)
    col_widths = [min(15, max(11, label_max_width * 1.3))] + [12] * len(ALL_NUMBERS)
    if debug:
        print(f"[DEBUG] 初始總欄寬: {sum(col_widths):.2f} pt")
    total_width = landscape(A4)[0] - 18  # 左右邊界 9pt + 9pt
    scale = total_width / sum(col_widths)
    col_widths = [w * scale for w in col_widths]
    if debug:
        print(f"[DEBUG] 縮放後總欄寬: {sum(col_widths):.2f} / 可用寬度: {total_width:.2f} pt")
        if sum(col_widths) > total_width:
            print("[WARNING] 表格總寬超出 A4 可用範圍，請縮小字體或欄寬")

    table = Table(data, colWidths=col_widths, repeatRows=1, hAlign='LEFT')
    style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'JhengHei'),
        ('FONTSIZE', (0, 0), (-1, -1), 6.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('BOX', (0, 0), (-1, -1), 1.2, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1.2, colors.black),
    ])
    for idx, (label, _) in enumerate(rows, start=1):
        bg = SECTION_COLORS.get(label)
        if bg:
            style.add('BACKGROUND', (0, idx), (-1, idx), bg)
    table.setStyle(style)
    table._argW = col_widths
    content.append(table)

    doc = SimpleDocTemplate(str(PDF_PATH), pagesize=landscape(A4), leftMargin=9, rightMargin=9, topMargin=6, bottomMargin=6)
    doc.build(content)

# 🚀 主程式
if __name__ == "__main__":
    stats, last_date = collect_weekday_number_counts()
    rows = build_report_rows(stats)
    generate_pdf(rows, last_date, debug=True)
    print(f"[INFO] PDF 已產出：{PDF_PATH}")
