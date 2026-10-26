# -*- coding: utf-8 -*-
"""md → word(docx via pandoc) + pdf(weasyprint, 中文样式) 全套转换。
用法：python build_docs.py  （在 course/ 目录执行）
"""
import subprocess, os, sys, glob

try:
    from xhtml2pdf import pisa
except ImportError:
    sys.exit("需要 xhtml2pdf：pip install xhtml2pdf")
import markdown

CSS = """
@page { size: a4 portrait; margin: 2cm; @frame footer_frame { -pdf-frame-content: footer; bottom: 0.6cm; height: 0.8cm; left: 2cm; width: 16cm; } }
body { font-family: "Microsoft YaHei"; font-size: 10.5pt; color: #222; line-height: 1.6; }
h1 { color: #1F3A5F; font-size: 19pt; border-bottom: 2px solid #1F3A5F; padding-bottom: 4px; }
h2 { color: #0E7C7B; font-size: 14pt; margin-top: 14px; }
h3 { color: #1F3A5F; font-size: 12pt; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 6px 0; }
th { background-color: #1F3A5F; color: white; padding: 4px 6px; border: 0.5pt solid #999; }
td { padding: 3px 6px; border: 0.5pt solid #bbb; }
pre, code { font-family: Consolas; font-size: 9pt; background-color: #EEF1F4; }
blockquote { color: #555; background-color: #FDF0E7; padding: 6px 10px; }
"""

def convert_one(src, out_word, out_pdf):
    base = os.path.splitext(os.path.basename(src))[0]
    # word
    subprocess.run(["pandoc", src, "-o", out_word, "--metadata", "title=" + base], check=True)
    # md -> html -> pdf
    with open(src, encoding="utf-8") as f:
        md = f.read()
    html_body = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"])
    html = ("<html><head><meta charset='utf-8'><style>%s</style></head><body>%s"
            "<div id='footer' style='text-align:center;font-size:8pt;color:#888;'>"
            "数字乡村综合服务平台项目实战 · 教学资料 · 第 <pdf:pagenumber> 页 / 共 <pdf:pagecount> 页</div>"
            "</body></html>" % (CSS, html_body))
    with open(out_pdf, "wb") as f:
        result = pisa.CreatePDF(html, dest=f, encoding="utf-8")
        if result.err:
            raise RuntimeError("xhtml2pdf errors: %d" % result.err)
    return base

def main():
    os.makedirs("word", exist_ok=True)
    os.makedirs("pdf", exist_ok=True)
    groups = [("docs", "docs/*.md"),
              ("worksheets", "worksheets/*.md"),
              ("assessments", "assessments/*.md"),
              ("sync", "sync/README.md")]
    n = 0
    for _, pattern in groups:
        for src in sorted(glob.glob(pattern)):
            base = os.path.splitext(os.path.basename(src))[0]
            safe = base.replace("/", "_")
            try:
                convert_one(src, os.path.join("word", safe + ".docx"), os.path.join("pdf", safe + ".pdf"))
                print("OK", safe)
                n += 1
            except Exception as e:
                print("FAIL", safe, str(e)[:120])
    print("DONE", n)

if __name__ == "__main__":
    main()