# 📦 匯入模組
from fpdf import FPDF
from pathlib import Path
from datetime import datetime

# 📁 全域變數
BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)
TODAY = datetime.today().strftime("%Y-%m-%d")
REPORT_PATH = REPORT_DIR / f"lotto539_report_{TODAY}.pdf"

# 🖨️ PDF 產生類別
class LottoPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "今彩539 分析報告", ln=True, align="C")
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"產出日期：{TODAY}", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"第 {self.page_no()} 頁", align="C")

    def section_title(self, title):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)

    def section_body(self, lines):
        self.set_font("Arial", "", 12)
        for line in lines:
            self.cell(0, 8, line, ln=True)
        self.ln(5)

# 🧾 模擬內容填入（可替換成真實分析結果）
def get_sample_sections():
    return [
        ("熱門號碼（前5）", ["號碼 17 ➜ 184 次", "號碼 29 ➜ 181 次", "號碼 23 ➜ 178 次"]),
        ("冷門號碼（後5）", ["號碼 36 ➜ 121 次", "號碼 04 ➜ 119 次", "號碼 10 ➜ 118 次"]),
        ("奇偶比例", ["奇數：52.3%", "偶數：47.7%"]),
        ("尾數分布", ["尾數 3 ➜ 139 次", "尾數 7 ➜ 130 次", "尾數 9 ➜ 124 次"]),
        ("連號期數", ["含連號的期數共 689 期"]),
        ("區間分布", ["01–10：872 次", "11–20：993 次", "21–30：1502 次", "31–39：1633 次"]),
        ("星期分布", ["星期一：203 期", "星期五：198 期"])
    ]

# 📝 產生 PDF 主函式
def generate_pdf_report():
    pdf = LottoPDF()
    pdf.add_page()

    for title, content in get_sample_sections():
        pdf.section_title(title)
        pdf.section_body(content)

    pdf.output(str(REPORT_PATH))
    print(f"✅ PDF 已產出：{REPORT_PATH}")

# 🚀 主程式
if __name__ == "__main__":
    generate_pdf_report()
