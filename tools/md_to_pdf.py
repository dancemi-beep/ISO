import os
import sys
from fpdf import FPDF

def md_to_pdf(md_path, pdf_path):
    """
    極簡 Markdown 轉 PDF (處理繁體中文與基礎格式)
    """
    class PDF(FPDF):
        def header(self):
            # 可以在這裡加入 Logo 或標題
            pass

    pdf = PDF()
    pdf.add_page()
    
    # 使用包含繁體中文的字體 (嘗試使用系統常見字體)
    # macOS 常見路徑
    font_paths = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/Library/Fonts/Microsoft/SimSun.ttf"
    ]
    
    font_loaded = False
    for fp in font_paths:
        if os.path.exists(fp):
            pdf.add_font("CustomFont", "", fp)
            pdf.set_font("CustomFont", size=12)
            font_loaded = True
            break
            
    if not font_loaded:
        pdf.set_font("Arial", size=12)
        print("警告: 找不到合適的中文字體，PDF 可能出現亂碼。")

    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            pdf.set_font(size=18)
            pdf.cell(0, 10, line[2:], ln=True)
            pdf.set_font(size=12)
        elif line.startswith("## "):
            pdf.set_font(size=16)
            pdf.cell(0, 10, line[3:], ln=True)
            pdf.set_font(size=12)
        elif line:
            # 處理一些 markdown 標示
            clean_line = line.replace("**", "").replace("__", "")
            pdf.multi_cell(0, 10, clean_line)
            pdf.ln(2)

    pdf.output(pdf_path)
    print(f"PDF 已生成: {pdf_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使用方式: python md_to_pdf.py <input.md> <output.pdf>")
    else:
        md_to_pdf(sys.argv[1], sys.argv[2])
